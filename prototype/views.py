import logging
from django.shortcuts import render, redirect
from django.template import add_to_builtins, TemplateDoesNotExist,\
	TemplateSyntaxError
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST, last_modified
from prototype.middleware import get_current_project
from prototype.decorators import toolbar, project_exists
from prototype.forms import FrontEndProjectForm

logger = logging.getLogger(__name__)

def project_lm(request):
	project = get_current_project()
	if project:
		return project.last_modified

@project_exists
@last_modified(project_lm)
@toolbar('projects')
def list_templates(request):
	add_to_builtins('prototype.template_tags.proto')

	project = get_current_project()

	if request.method == "POST":
		project_form = FrontEndProjectForm(request.POST, instance=project)

		if project_form.is_valid():
			project_form.save()

			return redirect('template_list')
	else:
		project_form = FrontEndProjectForm(instance=project)

	params = {
		'form': project_form
	}

	return render(request, 'prototype/index.html', params)

@require_POST
@project_exists
def build_static(request):
	project = get_current_project()
	build_url = settings.MEDIA_URL + project.build_static()
	return HttpResponse(build_url, content_type='text/plain')

@project_exists
@toolbar()
def show_template(request, template):
	# Add template tags (so we don't need to load them in each template)
	add_to_builtins('prototype.template_tags.proto')

	try:
		return render(request, template)
	except TemplateDoesNotExist:
		return render(request, "prototype/missing.html", {'current_template': template})
	except TemplateSyntaxError as e:
		params = {
			'current_template': template,
			'error_type': 'template syntax error',
			'error_detail': unicode(e)
		}
	except Exception as e:
		params = {
			'current_template': template,
			'error_type': 'unexpected error',
			'error_detail': unicode(e)
		}
	return render(request, "prototype/error.html", params)

@toolbar('projects')
def handle404(request):
	return render(request, '404.html')