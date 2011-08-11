import os
from django.db import models
from django.utils._os import safe_join

TEMPLATES_PATH = 'C:\\WebRoot\\templates\\%s\\www'

class Project(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255)
	
	def _get_template_dir(self):
		return TEMPLATES_PATH % self.slug
	template_dir = property(_get_template_dir)
	
	def _get_template_listing(self):
		# @todo: return template titles as well as file names
		tmpl_dir = self.template_dir
		return (path.split(".")[0] for path in os.listdir(tmpl_dir) if os.path.isfile(safe_join(tmpl_dir, path)))
	template_listing = property(_get_template_listing)
	
	def __unicode__(self):
		return u'%s' % self.name
	
	class Meta:
		ordering = ['name']
		