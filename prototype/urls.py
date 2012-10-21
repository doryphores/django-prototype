from django.conf.urls.defaults import *

urlpatterns = patterns('prototype.views',
	url(r'^$', 'list_templates', name='template_list'),
	url(r'^(?P<template>[a-zA-Z0-9_-]+)$', 'show_template', name='template'),
)
