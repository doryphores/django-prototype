from prototype.middleware import get_current_project

def project(request):
	project = get_current_project()
	if project:
		return {
			'project': project,
			'data': project.data
		}
	else:
		return {}