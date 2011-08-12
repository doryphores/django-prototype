from front.models import Project
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.template import add_to_builtins

def list_templates(request):
	project_slug = request.get_host().split(".")[0]
	project = Project.objects.get(slug=project_slug)
	
	return render(request, 'index.html', { 'project': project })

def show_template(request, page):
	add_to_builtins('front.template_tags.proto')
	return render(request, page)

@require_POST
def build_assets(request):
	project_slug = request.get_host().split(".")[0]
	project = Project.objects.get(slug=project_slug)
	
	project.build_assets()
	
	return redirect('list_templates')