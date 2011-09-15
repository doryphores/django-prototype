from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader
from prototype.middleware import get_current_request
from django.template.loaders import filesystem
from prototype.models import Project

class Loader(BaseLoader):
	is_usable = True

	def load_template_source(self, template_name, template_dirs=None):
		request = get_current_request()
		
		project = Project.objects.get_current(request)
		
		if project:
			if template_dirs is None:
				template_dirs = (project.template_dir, )
			else:
				template_dirs += (project.template_dir, )
			
			return filesystem.load_template_source(template_name, template_dirs)
		
		raise TemplateDoesNotExist(template_name)