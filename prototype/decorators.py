from functools import wraps
from django.template.loader import render_to_string
import re
from django.template.context import RequestContext
from django.conf import settings

def toolbar():
	def _toolbar_controller(viewfunc):
		def _toolbar_controlled(request, *args, **kwargs):
			response = viewfunc(request, *args, **kwargs)
			
			# Render toolbar
			toolbar = render_to_string('prototype/toolbar.html', {'current_template': kwargs["template"]}, context_instance=RequestContext(request))
			
			# Inject the toolbar
			response.content = re.sub(r'(</(body|BODY)\>)', r'%s\1' % toolbar, response.content.decode(settings.FILE_CHARSET))
			
			return response
		return wraps(viewfunc)(_toolbar_controlled)
	return _toolbar_controller