from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect as redirect_to, redirect

from .forms import LoginForm , RegisterForm
from .models import MyUser
# Create your views here.
def auth_login(request):
	head_title = "Login"
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username,password=password)
		if user:
			login(request,user)
			if next_url:
				return redirect_to(next_url)	
			return redirect('home')
		else:
			pass

	context = {
		"head_title":head_title,
		"form": form,
	}
	template = "login.html"
	return render(request, template, context)


@login_required
def auth_logout(request):
	logout(request)
	return redirect_to('/')



def auth_register(request):
	head_title = "Register"
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password2']
		MyUser.objects.create_user(username=username, email=email, password=password)
		return redirect('login')

	context = {
		"head_title":head_title,
		'form':form,
	}
	template = "accounts/register_form.html"
	return render(request, template, context)


# @login_required(login_url='/staff/login/')
# def staff_home(request):
# 	head_title = "Staff Only"
# 	context = {
		
# 	}
# 	template = "home.html"
# 	return render(request, template, context)