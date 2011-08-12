import os
from django.db import models
from django.utils._os import safe_join
from django.conf import settings
import cssmin
import re
from shutil import copytree, ignore_patterns, rmtree
import codecs
import stat

TEMPLATES_PATH = 'C:\\WebRoot\\templates'

class Project(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255)
	
	project_root = models.CharField(max_length=255, blank=True, help_text="Location of project if different from %s" % safe_join(TEMPLATES_PATH, "[project_slug]"))
	templates_root = models.CharField(max_length=255, blank=True, default="www", help_text="The folder within the project where templates are stored")
	assets_root = models.CharField(max_length=255, blank=True, default="assets", help_text="The folder within the template root where assets are stored.")
	ignore_list = models.CharField(max_length=255, blank=True, default="images/content")
	
	def _get_template_dir(self):
		return safe_join(TEMPLATES_PATH, self.slug, self.templates_root)
	template_dir = property(_get_template_dir)
	
	def _get_template_listing(self):
		# @todo: return template titles as well as file names
		tmpl_dir = self.template_dir
		return (path.split(".")[0] for path in os.listdir(tmpl_dir) if os.path.isfile(safe_join(tmpl_dir, path)))
	template_listing = property(_get_template_listing)
	
	def get_build_path(self):
		return safe_join(settings.BUILD_PATH, "%s-%d" % (self.slug, self.pk))
	
	def init_build(self):
		build_path = self.get_build_path()
		if not os.path.isdir(build_path):
			os.mkdir(build_path)
		for filepath in os.listdir(build_path):
			filepath = os.path.join(build_path, filepath)
			if os.path.isdir(filepath):
				rmtree(filepath)
			else:
				os.unlink(filepath)
	
	def concatenate_css(self, file="screen.css"):
		# Prepare css
		css_dir = safe_join(self.template_dir, self.assets_root, "css")
		screen_css = open(safe_join(css_dir, file))
		p = re.compile('@import\s+"(.*?)".*', re.DOTALL)
		concat_css = ''.join([open(safe_join(css_dir, p.sub(r'\1', line))).read().decode(settings.FILE_CHARSET) for line in screen_css if line.find("@import") == 0])
		
		return cssmin.cssmin(concat_css)
	
	def build_assets(self):
		self.init_build()
		
		build_path = self.get_build_path()
		
		asset_dir = safe_join(self.template_dir, self.assets_root)
		copytree(asset_dir, safe_join(build_path, self.assets_root), ignore=ignore_patterns(self.ignore_list, '.svn', 'screen.css'))
		screen_css = codecs.open(safe_join(build_path, self.assets_root, "css", "screen.css"), encoding='utf-8', mode='w+')
		screen_css.write(self.concatenate_css())
	
	def __unicode__(self):
		return u'%s' % self.name
	
	class Meta:
		ordering = ['name']
		