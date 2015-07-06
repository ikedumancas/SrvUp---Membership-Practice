import datetime
from django.conf import settings
from django.utils import timezone

import braintree
braintree.Configuration.configure(braintree.Environment.Sandbox, # change Sandbox to Production on production mode
	merchant_id=settings.BRAINTREE_MERCHANT_ID,
	public_key=settings.BRAINTREE_PUBLIC_KEY,
	private_key=settings.BRAINTREE_PRIVATE_KEY)



from .signals import membership_dates_update


def check_membership_status(subscription_id):
    # checking in braintree
    sub = braintree.Subscription.find(subscription_id)
    if sub.status == "Active":
    	status = True
    	next_billing_date = sub.next_billing_date
    else:
    	status = False
    	next_billing_date = None
    return status, next_billing_date


def update_braintree_membership(user):
	membership = user.membership
	if membership.date_end <= timezone.now():
		subscription_id = user.usermerchantid.subscription_id
		status, next_billing_date = check_membership_status(subscription_id)
		if status:
			small_time = datetime.time(0,0,0,1)
			datetime_obj = datetime.datetime.combine(next_billing_date, small_time)
			new_next_billing_date = timezone.make_aware(datetime_obj, timezone.get_current_timezone())
			membership_dates_update.send(membership,new_date_start=new_next_billing_date)
		else:
			membership.update_status()
