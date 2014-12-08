from django.conf.urls import url, patterns
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from blog.models import Entry

info_dict = {
    'queryset': Entry.published.all(),
    'date_field': 'updated_on',
}

sitemaps = {
    'blog': GenericSitemap(info_dict, priority=0.5),
}

urlpatterns = patterns('',
    url(r'^$', 'blog.views.home', name='blog_home'),
    url(r'^archive/$', 'blog.views.archive', name='blog_archive'),
    url(r'^tags/(?P<slug>[-\w]+)/$', 'blog.views.tag', name='blog_tag'),
    url(ur'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\S]+)/$', 'blog.views.entry', name='blog_entry'),
) + patterns('django.contrib.sitemaps.views',                                   # Sitemap added
    url(r'sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    url(r'sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)
