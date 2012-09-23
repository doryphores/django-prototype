import re
from functools import wraps
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.conf import settings
from django.http import Http404
from prototype.models import Project
from prototype.middleware import get_current_project


def toolbar(type="templates"):
	"""
	Injects the toolbar into the generated HTML.
	Default type is the current project's template list.
	If type is 'projects', the toolbar will display a list of available projects.
	"""
	def _toolbar_controller(viewfunc):
		def _toolbar_controlled(request, *args, **kwargs):
			response = viewfunc(request, *args, **kwargs)

			if type == "projects":
				# Render toolbar
				toolbar = render_to_string('prototype/projects_toolbar.html', {'projects': Project.objects.all()}, context_instance=RequestContext(request))
			else:
				# Render toolbar
				toolbar = render_to_string('prototype/templates_toolbar.html', {'current_template': kwargs["template"]}, context_instance=RequestContext(request))

			# Inject the toolbar
			response.content = re.sub(r'(</(body|BODY)\>)', r'%s\1' % toolbar, response.content.decode(settings.FILE_CHARSET))

			return response
		return wraps(viewfunc)(_toolbar_controlled)
	return _toolbar_controller


def project_exists(viewfunc):
	"""
	Checks that the requested project exists and returns a 404 if not
	"""
	@wraps(viewfunc)
	def _project_exists(request, *args, **kwargs):
		if not get_current_project():
			raise Http404

		return viewfunc(request, *args, **kwargs)
	return _project_exists
