from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader
from front.middleware import get_current_request

class Loader(BaseLoader):
	is_usable = True

	def load_template_source(self, template_name, template_dirs=None):
		request = get_current_request()
		
		project = request.project
		
		if project:
			# Try adding html and html extension to template name
			tmpl_dir = project.template_dir
			for ext in ["", ".htm", ".html"]:
				filepath = "%s/%s%s" % (tmpl_dir, template_name, ext)
				try:
					file = open(filepath)
					try:
						return (file.read().decode(settings.FILE_CHARSET), filepath)
					finally:
						file.close()
				except IOError:
					pass
		
		raise TemplateDoesNotExist(template_name)