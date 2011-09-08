from django.shortcuts import render
from django.template import add_to_builtins, TemplateDoesNotExist,\
	TemplateSyntaxError
from prototype.decorators import toolbar

def list_templates(request):
	add_to_builtins('prototype.template_tags.proto')
	
	return render(request, 'prototype/index.html')

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