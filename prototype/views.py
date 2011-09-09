from django.shortcuts import render, redirect
from django.template import add_to_builtins, TemplateDoesNotExist,\
	TemplateSyntaxError
from prototype.decorators import toolbar
from prototype.forms import ProjectForm

@toolbar('projects')
def list_templates(request):
	add_to_builtins('prototype.template_tags.proto')
	
	if request.method == "POST":
		project_form = ProjectForm(request.POST, instance=request.project)
		
		if project_form.is_valid():
			project_form.save()
			
			return redirect("template_list")
	else:
		project_form = ProjectForm(instance=request.project)
	
	params = {
		'project': request.project,
		'templates': request.project.templates,
		'form': project_form
	}
	
	return render(request, 'prototype/index.html', params)

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