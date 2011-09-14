from django.conf.urls.defaults import *

urlpatterns = patterns('prototype.views',
	url(r'^$', 'list_templates', name='template_list'),
	url(r'^update$', 'update_project', name='update_project'),
	url(r'^build$', 'build_static', name='build_static'),
	
	url(r'^(?P<template>[a-zA-Z0-9_-]+\.htm(l)?)$', 'show_template', name='template'),
)