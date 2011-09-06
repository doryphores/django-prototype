from prototype.models import Project
def data(request):
	project = Project.objects.get_current(request)
	if project:
		return {'data': project.data}
	else:
		return {}