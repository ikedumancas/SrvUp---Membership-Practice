from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect as redirect_to, redirect
from accounts.forms import RegisterForm, LoginForm
from accounts.models import MyUser
from videos.models import Video

from analytics.models import PageView
from analytics.signals import page_view
from comments.models import Comment

def home(request):
	head_title = "Home"
	if request.user.is_authenticated():
		recent_videos = request.user.pageview_set.get_recent_videos()
		recent_comments = Comment.objects.recent()
		popular_videos = PageView.objects.get_popular_videos()
		context = {
			"head_title":head_title,
			"recent_videos":recent_videos,
			"recent_comments":recent_comments,
			"popular_videos":popular_videos,
		}
		template = "home_logged_in.html"
	else:
		login_form = LoginForm()
		register_form = RegisterForm()
		context = {
			"head_title":head_title,
			'register_form':register_form,
			'login_form':login_form,
		}
		template = "home.html"
	return render(request, template, context)