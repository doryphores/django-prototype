import os
from django.db import models
from django.utils._os import safe_join
from django.conf import settings
import cssmin
import re
from shutil import copytree, ignore_patterns, rmtree
import codecs
import subprocess
import datetime

# Initialise project cache
PROJECT_CACHE = {}

class ProjectManager(models.Manager):
	
	def get_current(self, request):
		"""
		Returns the current ``Project`` based on
		the current request host.
		The ``Project`` object is cached the first
		time it's retrieved from the database.
		"""
		
		project_slug = ""
		
		# Extract project slug from host name (the first bit)
		m = re.match(r'([^\.]+)\.%s' % settings.PROTOTYPE_TEMPLATES_HOST, request.get_host())
		if m:
			project_slug = m.group(1)
		
		try:
			current_project = PROJECT_CACHE[project_slug]
		except KeyError:
			try:
				current_project = self.get(slug=project_slug)
				PROJECT_CACHE[project_slug] = current_project
			except Project.DoesNotExist:
				return None
		
		return current_project
	
	def clear_cache(self):
		"""Clears the ``Project`` object cache."""
		global PROJECT_CACHE
		PROJECT_CACHE = {}
		
class Project(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	
	project_root = models.CharField(max_length=255, blank=True, help_text="Location of project if different from %s" % safe_join(settings.PROTOTYPE_TEMPLATES_ROOT, "[project_slug]"))
	templates_root = models.CharField(max_length=255, blank=True, default="www", help_text="The folder within the project where templates are stored")
	assets_root = models.CharField(max_length=255, blank=True, default="assets", help_text="The folder within the template root where assets are stored.")
	
	tmpl_last_modified = None
	
	_template_listing = []
	
	objects = ProjectManager()
	
	def _get_template_dir(self):
		return safe_join(settings.PROTOTYPE_TEMPLATES_ROOT, self.slug, self.templates_root)
	template_dir = property(_get_template_dir)
	
	def _get_templates(self):
		tmpl_dir = self.template_dir
		
		file_list = [
			(
				path,
				datetime.datetime.fromtimestamp(os.path.getmtime(safe_join(tmpl_dir, path))),
			)
			for path in os.listdir(tmpl_dir) if os.path.isfile(safe_join(tmpl_dir, path))
		]
		
		last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(tmpl_dir))
		
		if not self.tmpl_last_modified or len(self._template_listing) != len(file_list) or last_modified > self.tmpl_last_modified:
			self._template_listing = [file[0].split(".")[0] for file in file_list]
			self.tmpl_last_modified = last_modified
		
		return self._template_listing
	templates = property(_get_templates)
	
	def update_wc(self):
		pipe = subprocess.Popen('svn update', shell=True, cwd=safe_join(settings.PROTOTYPE_TEMPLATES_ROOT, self.slug))
		pipe.wait()
		return
	
	def get_build_path(self):
		return safe_join(settings.PROTOTYPE_BUILD_PATH, "%s-%d" % (self.slug, self.pk))
	
	def init_build(self):
		build_path = self.get_build_path()
		if os.path.isdir(build_path):
			rmtree(build_path)
		
		os.mkdir(build_path)
	
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
		copytree(asset_dir, safe_join(build_path, self.assets_root), ignore=ignore_patterns('.svn', 'screen.css'))
		screen_css = codecs.open(safe_join(build_path, self.assets_root, "css", "screen.css"), encoding='utf-8', mode='w+')
		screen_css.write(self.concatenate_css())
	
	def save(self, *args, **kwargs):
		old_slug = None
		try:
			old_slug = Project.objects.get(pk=self.pk).slug
		except Project.DoesNotExist:
			pass
		super(Project, self).save(*args, **kwargs)
		if old_slug and old_slug in PROJECT_CACHE:
			del PROJECT_CACHE[old_slug]
	
	def delete(self):
		slug = self.slug
		super(Project, self).delete()
		try:
			del PROJECT_CACHE[slug]
		except KeyError:
			pass
	
	def __unicode__(self):
		return u'%s' % self.name
	
	class Meta:
		ordering = ['name']