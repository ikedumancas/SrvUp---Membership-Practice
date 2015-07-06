from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.crypto import get_random_string

from .models import Membership, Transaction, UserMerchantId
from .signals import membership_dates_update
from accounts.models import MyUser
from notifications.signals import notify
# Create your views here.

# BRAINTREE CONFIG
import braintree
braintree.Configuration.configure(braintree.Environment.Sandbox, # change Sandbox to Production on production mode
	merchant_id=settings.BRAINTREE_MERCHANT_ID,
	public_key=settings.BRAINTREE_PUBLIC_KEY,
	private_key=settings.BRAINTREE_PRIVATE_KEY)
PLAN_ID = "monthly_plan"


def get_or_create_user_transaction(user, braintree_transaction):
	trans_id = braintree_transaction.id
	try:
		trans = Transaction.objects.get(user=user, transaction_id=trans_id)
		created = False
	except:
		created = True
		payment_type = braintree_transaction.payment_instrument_type
		amount = braintree_transaction.amount
		if payment_type == braintree.PaymentInstrumentType.PayPalAccount:
			trans = Transaction.objects.create_new(user, trans_id, amount, "PayPal")
			trans_success = trans.success
			trans_timestamp = trans.timestamp
		elif payment_type ==braintree.PaymentInstrumentType.CreditCard:
			credit_card_details = braintree_transaction.credit_card_details
			card_type = credit_card_details.card_type
			last_4 = credit_card_details.last_4
			trans = Transaction.objects.create_new(user,trans_id, amount, card_type, last_four=last_4)
			trans_success = trans.success
			trans_timestamp = trans.timestamp
		else:
			created = False
			trans = None
	return trans, created


def update_transaction_user(user):
	bt_transactions = braintree.Transaction.search(
			braintree.TransactionSearch.customer_id == user.usermerchantid.customer_id
		)
	try:
		user_transactions = user.transaction_set.all()
	except:
		user_transactions = None

	if user_transactions is not None and bt_transactions is not None:
		if not bt_transactions.maximum_size <= user_transactions.count():
			for bt_tran in bt_transactions.items:
				new_tran, created = get_or_create_user_transaction(user,bt_tran)



@login_required
def upgrade(request):
	head_title = "Upgrade Account"
	update_transaction_user(request.user)
	try:
		merchant_obj = UserMerchantId.objects.get(user=request.user)
	except :
		messages.error(request, "There was an error with your account. Please contact us.")
		return redirect("contact_us")
	merchant_customer_id = merchant_obj.customer_id
	print merchant_customer_id
	client_token = braintree.ClientToken.generate({
			"customer_id": merchant_customer_id
		})
	#print client_token
	if request.method == "POST":
		nonce = request.POST.get("payment_method_nonce", None)
		if nonce is None:
			messages.error(request, "An error occued, please try again")
			return redirect("account_upgrade")
		else:
			payment_method_result = braintree.PaymentMethod.create({
					"customer_id": merchant_customer_id,
					"payment_method_nonce": nonce,
					"options": {
						"make_default": True
					}
				})
			if not payment_method_result.is_success:
				messages.error(request, "An error occured: %s" %(payment_method_result.message))
				return redirect("account_upgrade")

			the_token = payment_method_result.payment_method.token
			current_sub_id = merchant_obj.subscription_id
			current_plan_id = merchant_obj.plan_id
			did_create_sub = False
			did_update_sub = False
			trans_success = False
			trans_timestamp = None

			try:
				current_subscription = braintree.Subscription.find(current_sub_id)
				sub_status = current_subscription.status
			except:
				current_subscription = None
				sub_status = None

			if current_subscription and sub_status == "Active":
				update_sub = braintree.Subscription.update(current_sub_id, {
							"payment_method_token": the_token,
						})
				did_update_sub = True
			else:
				create_sub = braintree.Subscription.create({
						"payment_method_token": the_token,
						"plan_id": PLAN_ID
					})
				did_create_sub = True

			if did_create_sub or did_update_sub:
				membership_instance, created = Membership.objects.get_or_create(user=request.user)


			if did_update_sub and not did_create_sub:
				messages.success(request, "Your plan has been updated")
				membership_dates_update.send(membership_instance, new_date_start=timezone.now())
				return redirect("billing_history")
			elif did_create_sub and not did_update_sub:
				merchant_obj.subscription_id = create_sub.subscription.id
				merchant_obj.plan_id = PLAN_ID
				merchant_obj.save()
				payment_type = create_sub.subscription.transactions[0].payment_instrument_type
				trans_id = create_sub.subscription.transactions[0].id
				sub_id = create_sub.subscription.id
				sub_amount = create_sub.subscription.price
				if payment_type == braintree.PaymentInstrumentType.PayPalAccount:
					trans = Transaction.objects.create_new(request.user, trans_id, sub_amount, "PayPal")
					trans_success = trans.success
					trans_timestamp = trans.timestamp
				elif payment_type ==braintree.PaymentInstrumentType.CreditCard:
					credit_card_details = create_sub.subscription.transactions[0].credit_card_details
					card_type = credit_card_details.card_type
					last_4 = credit_card_details.last_4
					trans = Transaction.objects.create_new(request.user,trans_id, sub_amount, card_type, last_four=last_4)
					trans_success = trans.success
					trans_timestamp = trans.timestamp
				else:
					trans_success = False
				membership_dates_update.send(membership_instance, new_date_start=trans_timestamp)
				messages.success(request, "Welcome to our service")
				return redirect("billing_history")
			else:
				messages.error(request, "An error occued, please try again")
				return redirect("account_upgrade")
	context = {
		"head_title":head_title,
		"client_token":client_token,
	}
	template = "billing/upgrade.html"
	return render(request, template, context)

@login_required
def history(request):
	head_title = "Billing History"
	queryset = Transaction.objects.filter(user=request.user, success=True)
	context = {
		"head_title":head_title,
		"queryset":queryset,
	}
	template = "billing/history.html"
	return render(request, template, context)