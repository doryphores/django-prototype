import os
from django.conf import settings
from django.template.loader import BaseLoader, TemplateDoesNotExist
from prototype.middleware import get_current_project


class Loader(BaseLoader):
	is_usable = True

	def get_template_sources(self, template_name, template_dirs=None):
		project = get_current_project()

		try:
			f = "%s/%s" % (project.templates_root, template_name)
			if os.path.isfile(f):
				return f
		except:
			pass

	def load_template_source(self, template_name, template_dirs=None):
		filepath = self.get_template_sources(template_name, template_dirs)
		if filepath:
			try:
				file = open(filepath)
				try:
					return (file.read().decode(settings.FILE_CHARSET), filepath)
				finally:
					file.close()
			except IOError:
				pass
		raise TemplateDoesNotExist(template_name)
