from front.models import Project
from django.shortcuts import render

def list_templates(request):
	project_slug = request.get_host().split(".")[0]
	project = Project.objects.get(slug=project_slug)
	
	return render(request, 'index.html', { 'project': project })

def show_template(request, page):
	return render(request, page)