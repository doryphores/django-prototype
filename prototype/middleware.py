from prototype.models import Project
try:
	from threading import local
except ImportError:
	from django.utils._threading_local import local

_thread_locals = local()


def get_current_project():
	return getattr(_thread_locals, 'project', None)


class ProjectMiddleware(object):
	def process_request(self, request):
		project = Project.objects.get_current(request)
		_thread_locals.project = project
