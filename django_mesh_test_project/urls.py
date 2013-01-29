#Django imports
from django.conf.urls import patterns, include, url
from django.contrib import admin

#App imports
#from ../django_mesh/models import Post   # wont work why?
#from django.contrib.sitemaps import Sitemap

#class MeshSitemap(Sitemap):
#    changefreq = "daily"
#    priority   = 0.5

#    def items(self):
#        return Post.objects.active()

#    def lastmod(self, post):
#        return post.last_edited

#from django.contrib.sitemaps import GenericSitemap

#sitemaps = {
#	'blog': GenericSitemap(
#				{
#					'queryset': Post.objects.active(),
#					'date_field': 'last_edited',
#				},
#				changefreq = 'daily',
#				priority = 0.5,
#			),
#}

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^comments/', include('django.contrib.comments.urls')),
	url(r'^django_mesh/', include('django_mesh.urls')),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
#	(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
