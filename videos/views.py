from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect as redirect_to, get_object_or_404

from .models import Video, Category, TaggedItem
from analytics.signals import page_view
from comments.forms import CommentForm
from comments.models import Comment
# Create your views here.


def video_detail(request, cat_slug,vid_slug):
	cat = get_object_or_404(Category, slug=cat_slug)
	obj = get_object_or_404(Video, slug=vid_slug, category=cat)
	page_view.send(request.user,
		page_path=request.get_full_path(),
		primary=obj,
		secondary=cat)
	head_title = obj.title
	context = {
		"head_title":head_title,
		"obj":obj,
	}
	template = "videos/video_detail.html"
	try:
		is_member = request.user.is_member
	except:
		is_member = False

	if obj.has_preview or is_member:
		if request.user.is_authenticated():
			comments = obj.comment_set.all()
			comment_form = CommentForm()
			context.update({
				"comments":comments,
				"comment_form":comment_form,
			})
	else:
		next_url = cat.get_absolute_url()
		messages.warning(request, 'You have to be a member to access this content. <a href="%s">Upgrade your account here</a>' %(reverse('account_upgrade'))) 
		return redirect_to(next_url)
		# return HttpResponseRedirect("%s?next=%s"%(reverse('account_upgrade'), next_url)) # activate this if you want the user to go to upgrade
	return render(request, template, context)


def category_detail(request, cat_slug):
	head_title = "Detailed"
	path = request.get_full_path()
	comments = Comment.objects.filter(path=path)
	obj = get_object_or_404(Category, slug=cat_slug)
	queryset = obj.video_set.all()
	page_view.send(request.user,
		page_path=request.get_full_path(),
		primary=obj,)
	context  = {
		"head_title":head_title,
		"obj":obj,
		"queryset":queryset,
		"comments":comments,
	}
	template = "videos/category_detail.html"
	return render(request, template, context)


def category_list(request):
	head_title = "Home"
	queryset   = Category.objects.all()
	context    = {
		"head_title":head_title,
		"queryset":queryset,
	}
	template = "videos/category_list.html"
	return render(request, template, context)


# def video_create(request):
# 	head_title = "Login"
# 	context = {
# 		"head_title":head_title,
# 	}
# 	template = "video_single.html"
# 	return render(request, template, context)


# def video_edit(request):
# 	head_title = "Login"
# 	context = {
# 		"head_title":head_title,
# 	}
# 	template = "video_single.html"
# 	return render(request, template, context)