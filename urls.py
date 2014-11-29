from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'blog.views.home', name='blog_home'),
    url(r'^archive/$', 'blog.views.archive', name='blog_archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'blog.views.entry', name='blog_entry'),
)
