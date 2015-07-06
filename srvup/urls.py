from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    # Examples:
    # url(r'^$', TemplateView.as_view(template_name='about.html'), name='home'), #this can be used on Static pages like about page
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', 'srvup.views.home', name='home'),
    url(r'^contact_us/$', TemplateView.as_view(template_name='contact_us.html'), name='contact_us'), #this can be used on Static pages like about page
    # url(r'^staff/$', 'accounts.views.staff_home', name='staff_home'),

    # videos url
    url(r'^categories/$', 'videos.views.category_list', name='category_list'),
    url(r'^categories/(?P<cat_slug>[\w-]+)/$', 'videos.views.category_detail', name='category_detail'),
    url(r'^categories/(?P<cat_slug>[\w-]+)/(?P<vid_slug>[\w-]+)/$', 'videos.views.video_detail', name='video_detail'),

    url(r'^comment/(?P<id>\d+)/$', 'comments.views.comment_thread', name='comment_thread'),
    url(r'^comment/create/$', 'comments.views.comment_create_view', name='comment_create'),

    # notifications urls
    url(r'^notifications/$', 'notifications.views.all', name='notifications_all'),
    url(r'^notifications/ajax/$', 'notifications.views.get_notification_ajax', name='notifications_ajax'),
    url(r'^notifications/ajax/count$', 'notifications.views.get_notification_ajax', name='notifications_ajax_count'),
    url(r'^notifications/read/all/$', 'notifications.views.read_all', name='notifications_read_all'),
    url(r'^notifications/read/(?P<id>\d+)/$', 'notifications.views.read', name='notifications_read'),

    # billing urls
    url(r'^upgrade/$', 'billing.views.upgrade', name='account_upgrade'),
    url(r'^billing/$', 'billing.views.history', name='billing_history'),


    # authentication urls
    url(r'^login/$', 'accounts.views.auth_login', name='login'),
    url(r'^logout/$', 'accounts.views.auth_logout', name='logout'),
    url(r'^register/$', 'accounts.views.auth_register', name='register'),

    # django admin for developers
    url(r'^developeronly/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)