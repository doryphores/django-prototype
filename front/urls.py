from django.conf.urls.defaults import *

urlpatterns = patterns('front.views',
	url(r'^$', 'list_templates', name='list_templates'),
	url(r'^build$', 'build_assets', name='build_assets'),
	url(r'^(?P<page>[a-zA-Z0-9_-]+)\.htm$', 'show_template', name='template'),
	url(r'^(?P<page>[a-zA-Z0-9_-]+)\.html$', 'show_template'),
)