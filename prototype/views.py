from django.shortcuts import render
from django.template import add_to_builtins
from django.template.loader import render_to_string
import re
from django.conf import settings
from django.template.context import RequestContext

def list_templates(request):
	return render(request, 'prototype/index.html')

def show_template(request, page):
	# Add template tags (so we don't need to load them in each template)
	add_to_builtins('prototype.template_tags.proto')
	return add_toolbar(render(request, page), request)

def add_toolbar(response, request):
	# Render the toolbar
	toolbar = render_to_string('prototype/toolbar.html', context_instance=RequestContext(request))
	
	# Inject the toolbar
	response.content = re.sub(r'(</(body|BODY)\>)', r'%s\1' % toolbar, response.content.decode(settings.FILE_CHARSET))
	
	return response