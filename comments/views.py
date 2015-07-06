from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect as redirect_to

# Create your views here.
from accounts.models import MyUser
from videos.views import Category, Video
from notifications.signals import notify

from .models import Comment
from .forms import CommentForm

@login_required
def comment_thread(request,id):
	head_title   = 'View Comment Thread'
	comment_form = CommentForm(request.POST or None)
	try:
		if comment_form.is_valid():
			parent_id      = request.POST.get('parent_id')
			parent_comment = Comment.objects.get(id=parent_id)
			comment_text   = comment_form.cleaned_data['comment']
			new_comment    = Comment.objects.create_comment(
				user   =request.user, 
				text   =comment_text, 
				path   = parent_comment.origin, 
				video  = parent_comment.video,
				parent = parent_comment
			)
			return redirect_to(parent_comment.get_absolute_url())
		comment = Comment.objects.get(id=id)
		context = {
			'head_title':head_title,
			'comment':comment,
			'comment_form':comment_form,
		}
		template = "comments/comment_thread.html"
		return render(request, template, context)	
	except:
		raise Http404

@login_required
def comment_create_view(request):
	if request.method == 'POST':
		parent_id      = request.POST.get('parent_id')
		video_id       = request.POST.get('video_id')
		origin_path    = request.POST.get('origin_path')
		redirect_url   = origin_path
		parent_comment = None
		video          = None
		comment_form   = CommentForm(request.POST)
		
		if comment_form.is_valid():
			if video_id:
				try:
					video = Video.objects.get(id=video_id)
				except:
					messages.error(request, 'There was an error with your comment for this video.')
			if parent_id:
				try:
					parent_comment = Comment.objects.get(id=parent_id)
					video          = parent_comment.video
					origin_path    = parent_comment.origin
				except:
					messages.error(request, 'There was an error with your reply for this comment.')
			comment_text = comment_form.cleaned_data['comment']
			new_comment  = Comment.objects.create_comment(
				user   = request.user, 
				text   = comment_text, 
				path   = origin_path, 
				video  = video,
				parent = parent_comment,
			)
			if new_comment.is_child:
				affected_users = parent_comment.get_affected_users()
				notify.send(
					request.user,
					action=new_comment,
					verb='replied to',
					target=parent_comment,
					affected_users = affected_users,
					recipient=parent_comment.user,)
				redirect_url = parent_comment.get_absolute_url()
			else:
				notify.send(
					request.user,
					action=new_comment,
					verb='commented on',
					target=video,
					recipient=MyUser.objects.get(username="admin"))
				redirect_url = new_comment.get_absolute_url()
				
			messages.success(request, 'Your comment has been added.')
			# messages.success(request, 'Your comment has been added.', extra_tags='safe') # NOTE: add extra_tags='safe' if you add html to message
		else:
			messages.error(request, 'There was an error with your comment.')
		return redirect_to(redirect_url)
	raise Http404
