from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import truncatechars

from videos.models import Video

# Create your models here.

class CommentManager(models.Manager):
	def all(self):
		return super(CommentManager,self).filter(active=True).filter(parent=None)

	def recent(self):
		return self.all().reverse()[:6]

	def create_comment(self, user=None, text=None, path=None, video=None, parent=None):
		if not path:
			raise ValueError('Must include a path when adding a Comment')
		if not user:
			raise ValueError('Must include a user when adding a Comment')
		comment = self.model(
			user = user,
			path = path,
			text = text,
		)
		if video:
			comment.video = video
		if parent:
			comment.parent = parent	
		comment.save(using=self._db)
		return comment



class Comment(models.Model):
	user         = models.ForeignKey(settings.AUTH_USER_MODEL)
	parent       = models.ForeignKey('self', null=True, blank=True)
	path         = models.CharField(max_length=350)
	video        = models.ForeignKey(Video, null=True, blank=True)
	text         = models.TextField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated      = models.DateTimeField(auto_now=True, auto_now_add=False)
	active       = models.BooleanField(default=True)

	objects = CommentManager()

	class Meta:
		ordering = ['timestamp']

	def __unicode__(self):
		return "%s" %(self.text)

	@property
	def is_child(self):
		if self.parent:
			return True
		return False

	# @property
	# def has_child(self):
	# 	try:
	# 		Comment.objects.filter(parent=self)
	# 		return True
	# 	except:
	# 		return False

	@property
	def origin(self):
	    return self.path

	@property
	def preview(self):
		return truncatechars(self.text,100)
	
	def get_absolute_url(self):
		return reverse('comment_thread', kwargs={"id":self.id})

	def get_children(self):
		if self.is_child:
			return None
		return Comment.objects.filter(parent=self)

	def get_affected_users(self):
		"""
		Comment must be a parent to get affected users.
		"""
		comment_children = self.get_children();
		if comment_children is not None:
			users = []
			for comment in comment_children:
				if comment.user in users:
					pass
				else:
					users.append(comment.user)
			return users