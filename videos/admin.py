from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.
from .models import Category, Video, TaggedItem


class TaggedItemInline(GenericTabularInline):
	model = TaggedItem

class VideoInline(admin.TabularInline):
	model = Video

class CategoryAdmin(admin.ModelAdmin):
	inlines = [TaggedItemInline, VideoInline,]
	prepopulated_fields = {
		'slug':['title',],
	}
	class Meta:
		model = Category


class VideoAdmin(admin.ModelAdmin):
	inlines = [TaggedItemInline,]
	list_display = ["__unicode__", "category", "slug"]
	fields = [
		'order',
		'title',
		'share_message',
		'embed_code',
		'slug',
		'category',
		'active',
		'featured',
		'free_preview',
	]

	prepopulated_fields = {
		'slug':['title',],
	}

	class Meta:
		model = Video


admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)