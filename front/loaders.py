from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader
from front.models import Project
from front.middleware import get_current_request

class Loader(BaseLoader):
	is_usable = True

	def load_template_source(self, template_name, template_dirs=None):
		# Get host name from current request
		host = get_current_request().get_host()
		
		# Check that the host name points to a project
		if settings.TEMPLATES_HOST in host:
			# Extract project slug from host name (the first bit)
			project_slug = host.split(".")[0]
			
			try:
				# Get project from DB
				project = Project.objects.get(slug=project_slug)
			except Project.DoesNotExist:
				pass
			else:
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