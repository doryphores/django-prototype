from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader
from prototype.middleware import get_current_project
from django.template.loaders import filesystem

class Loader(BaseLoader):
	is_usable = True

	def load_template_source(self, template_name, template_dirs=None):
		project = get_current_project()
		
		if project:
			if template_dirs is None:
				template_dirs = (project.templates_root, )
			else:
				template_dirs += (project.templates_root, )
			
			return filesystem.load_template_source(template_name, template_dirs)
		
		raise TemplateDoesNotExist(template_name)