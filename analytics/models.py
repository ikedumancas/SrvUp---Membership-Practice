from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from django.template.defaultfilters import mark_safe

from videos.models import Video, Category
from .signals import page_view

# Create your models here.

class PageViewQuerySet(models.query.QuerySet):
	def videos(self):
		content_type = ContentType.objects.get_for_model(Video)
		return self.filter(primary_content_type=content_type)

	def categories(self):
		content_type = ContentType.objects.get_for_model(Category)
		return self.filter(primary_content_type=content_type)	


class PageViewManager(models.Manager):
	def get_queryset(self):
		return PageViewQuerySet(self.model, using=self._db)

	def get_videos(self):
		videos = []
		for video in self.get_queryset().videos():
			if video.primary_object not in videos:
				videos.append(video.primary_object)
		return videos

	def get_categories(self):
		categories = []
		for category in self.get_queryset().categories():
			if category.primary_object not in categories:
				categories.append(category.primary_object)
		return categories

	def get_recent_videos(self):
		return self.get_videos()[:6]

	def get_popular_videos(self):
		video_type = ContentType.objects.get_for_model(Video)
		popular_videos_id = self.get_queryset().filter(primary_content_type=video_type)\
		 .values("primary_object_id").annotate(view_count=Count("primary_object_id"))\
		 .order_by("-view_count")
		popular_videos = []
		for item in popular_videos_id:
			try:
				video = Video.objects.get(id=item['primary_object_id'])
				popular_videos.append(video)
			except:
				pass
		return popular_videos

	

class PageView(models.Model):
	path = models.CharField(max_length=350)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	
	primary_content_type = models.ForeignKey(ContentType, related_name='primary_obj',null=True, blank=True)
	primary_object_id    = models.PositiveIntegerField(null=True, blank=True)
	primary_object       = GenericForeignKey("primary_content_type", "primary_object_id")

	secondary_content_type = models.ForeignKey(ContentType, related_name='secondary_obj',null=True, blank=True)
	secondary_object_id    = models.PositiveIntegerField(null=True, blank=True)
	secondary_object       = GenericForeignKey("secondary_content_type", "secondary_object_id")

	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PageViewManager()

	class Meta:
		ordering = ['-timestamp']

	def __unicode__(self):
		return self.path


def page_view_received(sender, **kwargs):
	page_path = kwargs.pop("page_path")
	user = sender
	new_page_view = PageView(path = page_path)
	if user.is_authenticated():
		new_page_view.user = user

	for opt in ("primary", "secondary"):
		try:
			obj = kwargs[opt]
			if obj is not None:
				setattr(new_page_view, "%s_content_type" %opt, ContentType.objects.get_for_model(obj))
				setattr(new_page_view, "%s_object_id" %opt, obj.id)
		except:
			pass
	new_page_view.save()


page_view.connect(page_view_received)