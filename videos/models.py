import urllib2
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import mark_safe
from django.utils.text import slugify

from .utils import get_video_for_direction
# Create your models here.


class VideoQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(featured=True)

	def has_embed(self):
		return self.filter(embed_code__isnull = False).exclude(embed_code__exact="")


class VideoManager(models.Manager):
	def get_queryset(self):
		return VideoQuerySet(self.model, using=self._db)

	def get_featured(self):
		# Video.objects.filter(featured=True)
		# return super(VideoManager, self).filter(featured=True)
		return self.get_queryset().active().featured()

	def all(self):
		return self.get_queryset().active().has_embed()


DEFAULT_SHARE_MESSAGE = "Check out this awesome video."

class Video(models.Model):
	title         = models.CharField(max_length=120)
	order         = models.PositiveIntegerField(default=1)
	embed_code    = models.CharField(max_length=500, null=True, blank=True)
	share_message = models.TextField(default=DEFAULT_SHARE_MESSAGE)
	slug          = models.SlugField(null=True, blank=True)
	tags          = GenericRelation("TaggedItem", null=True, blank=True)
	active        = models.BooleanField(default=True)
	featured      = models.BooleanField(default=False)
	free_preview  = models.BooleanField(default=False)
	category      = models.ForeignKey('Category', default=1)
	timestamp  = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated       = models.DateTimeField(auto_now=True, auto_now_add=False)

	objects = VideoManager()

	class Meta:
		unique_together = ('slug', 'category')
		ordering = ['order', '-timestamp']

	def __unicode__(self):
		return self.title

	@property
	def safe_embed(self):
		return mark_safe(self.embed_code)

	def get_absolute_url(self):
		return reverse('video_detail', kwargs={"vid_slug":self.slug, "cat_slug":self.category.slug})

	def get_full_url(self):
		return "%s%s" %(settings.FULL_DOMAIN_NAME, self.get_absolute_url())

	def get_share_message(self):
		return urllib2.quote("%s %s" %(self.share_message, self.get_full_url()))

	def get_next_url(self):
		next_video = get_video_for_direction(self,"next")
		if next_video is not None:
			return next_video.get_absolute_url()
		return '#'

	def get_prev_url(self):
		prev_video = get_video_for_direction(self,"prev")
		if prev_video is not None:
			return prev_video.get_absolute_url()
		return '#'

	@property
	def has_preview(self):
		if self.free_preview:
			return True
		return False



def video_post_save_receiver(sender, instance, created, *args, **kwargs):
	if created:
		slug_title = slugify(instance.title)
		new_slug = "%s %s %s" %(instance.title, instance.category.slug, instance.id)
		try:
			obj = Video.objects.get(slug=slug_title, category=instance.category)
			instance.slug = slugify(new_slug)
			instance.save()
		except Video.DoesNotExist:
			instance.slug = slug_title
			instance.save()
		except Video.MultipltObjectsReturned:
			instance.slug = slugify(new_slug)
			instance.save()
		except:
			pass
	
post_save.connect(video_post_save_receiver, sender=Video)



class CategoryQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(featured=True)


class CategoryManager(models.Manager):
	def get_queryset(self):
		return CategoryQuerySet(self.model, using=self._db)

	def get_featured(self):
		return self.get_queryset().active().featured()

	def all(self):
		return self.get_queryset().active()


class Category(models.Model):
	title        = models.CharField(max_length=120)
	description  = models.TextField(max_length=5000, null=True, blank=True)
	tags         = GenericRelation("TaggedItem", null=True, blank=True)
	slug         = models.SlugField(unique=True)
	image        = models.ImageField(upload_to='images/', null=True, blank=True)
	active       = models.BooleanField(default=True)
	featured     = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated      = models.DateTimeField(auto_now=True, auto_now_add=False)

	objects = CategoryManager()

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('category_detail', kwargs={"cat_slug":self.slug})

	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.image)


TAG_CHOICES = (
	('python', 'python'),
	('django', 'django'),
	('html', 'html'),
	('css', 'css'),
	('javascript', 'javascript'),
	('bootstrap', 'bootstrap'),
)

class TaggedItem(models.Model):
	tag = models.SlugField(choices=TAG_CHOICES)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	def __unicode__(self):
		return self.tag