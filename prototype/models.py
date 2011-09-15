import os
from django.db import models
from django.utils._os import safe_join
from django.conf import settings
import cssmin
import re
from shutil import copytree, ignore_patterns, rmtree
import codecs
import subprocess
import logging
from threading import Lock
import json
from prototype import utils
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.cache import cache

logger = logging.getLogger(__name__)

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
		m = re.match(r'([^\.]+)\.%s' % settings.PROTOTYPE_PROJECTS_HOST, request.get_host())
		if m:
			project_slug = m.group(1)
		
		current_project = cache.get(project_slug)
		
		if not current_project:
			try:
				current_project = self.get(slug=project_slug)
				logger.debug('Loaded project %s into cache' % current_project.name)
				cache.set(project_slug, current_project)
			except Project.DoesNotExist:
				return None
		
		return current_project

class Project(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	
	data_root = models.CharField(max_length=255, blank=True, default=settings.PROTOTYPE_DEFAULT_DATA_PATH, help_text="The folder within the project where mocking data files are stored")
	static_root = models.CharField(max_length=255, blank=True, default="static", help_text="The folder within the template root where static assets are stored")
	
	use_html_titles = models.BooleanField(default=True, verbose_name='Titles', help_text="Which method to use to display template titles")
	
	tmpl_last_modified = None
	data_last_modified = None
	
	_template_listing = []
	_data_store = {}
	
	template_lock = Lock()
	data_lock = Lock()
	build_lock = Lock()
	
	objects = ProjectManager()
	
	def _get_template_dir(self):
		return os.path.join(settings.PROTOTYPE_PROJECTS_ROOT, self.slug, settings.PROTOTYPE_TEMPLATES_PATH)
	template_dir = property(_get_template_dir)
	
	def get_absolute_url(self):
		return 'http://%s.%s' % (self.slug, settings.PROTOTYPE_PROJECTS_HOST)
	
	def _get_templates(self):
		tmpl_dir = self.template_dir
		
		# Get list of templates if modified
		file_list = utils.list_dir_if_changed(tmpl_dir, self.tmpl_last_modified, ["htm", "html"])
		
		if file_list:
			# Lock project as this isn't thread safe
			with self.template_lock:
				self._template_listing = [Template(file_name, self) for file_name in file_list[0]]
				self.tmpl_last_modified = file_list[1]
			
			logger.debug('Reloaded template list for project %s' % self.name)
			
			# Update cache
			cache.set(self.slug, self)
		
		return self._template_listing
	templates = property(_get_templates)
	
	def _get_data(self):
		data_path = os.path.join(settings.PROTOTYPE_PROJECTS_ROOT, self.slug, self.data_root)
		
		if os.path.isdir(data_path):
			file_list = utils.list_dir_if_changed(data_path, self.data_last_modified)
			
			if file_list:
				data_store = {}
				
				for file_name in file_list[0]:
					file_parts = file_name.split(".")
					with open(os.path.join(data_path, file_name)) as f:
						try:
							data_store[file_parts[0]] = json.load(f)
						except:
							data_store[file_parts[0]] = None
				
				with self.data_lock:
					self._data_store = data_store
					self.data_last_modified = file_list[1]
				
				logger.debug('Reloaded data store for project %s' % self.name)
				
				# Update cache
				cache.set(self.slug, self)
		
		return self._data_store
	data = property(_get_data)
	
	def get_build_path(self):
		return safe_join(settings.PROTOTYPE_BUILD_PATH, self.slug)
	
	def init_build(self):
		build_path = self.get_build_path()
		if os.path.isdir(build_path):
			rmtree(build_path)
		
		return build_path
	
	def prepare_css(self, file="screen.css"):
		# Prepare css
		css_dir = safe_join(self.template_dir, self.static_root, "css")
		p = re.compile('@import\s+"(.*?)".*', re.DOTALL)
		concat_css = ""
		with open(safe_join(css_dir, file)) as screen_css:
			for line in screen_css:
				if line.find("@import") == 0:
					with open(safe_join(css_dir, p.sub(r'\1', line))) as f:
						concat_css += f.read().decode(settings.FILE_CHARSET)
		
		return cssmin.cssmin(concat_css)
	
	def build_static(self):
		# Ensure this is thread safe
		with self.build_lock:
			build_path = self.init_build()
			
			asset_dir = safe_join(self.template_dir, self.static_root)
			
			# Copy all static assets
			copytree(asset_dir, build_path, ignore=ignore_patterns('.svn', 'images\\content'))
			
			# Concatenate and minify stylesheets to screen.min.css
			with codecs.open(safe_join(build_path, "css", "screen.min.css"), encoding='utf-8', mode='w+') as f:
				f.write(self.prepare_css())
			
			#build = (utils.zipdir(build_path), "build-%s.zip" % self.get_rev_number())
			
			path = 'builds/%s/build.zip' % self.slug
			
			if default_storage.exists(path):
				default_storage.delete(path)
			
			build = default_storage.save(path, ContentFile(utils.zipdir(build_path)))
		
		return build
	
	# SCM functions
	
	def update_wc(self):
		pipe = subprocess.Popen('svn update', shell=True, cwd=safe_join(settings.PROTOTYPE_PROJECTS_ROOT, self.slug))
		pipe.wait()
		return
	
	def get_rev_number(self):
		pipe = subprocess.Popen('svnversion', shell=True, cwd=safe_join(settings.PROTOTYPE_PROJECTS_ROOT, self.slug), stdout=subprocess.PIPE)
		return pipe.communicate()[0].strip(' \t\n\r')
	
	def save(self, *args, **kwargs):
		if self.pk:
			old_slug = Project.objects.get(pk=self.pk).slug
			cache.delete(old_slug)
		super(Project, self).save(*args, **kwargs)
		cache.delete(self.slug)
	
	def delete(self):
		cache.delete(self.slug)
		super(Project, self).delete()
	
	def __unicode__(self):
		return u'%s' % self.name
	
	class Meta:
		ordering = ['name']


class Template(object):
	project = None
	
	title = None
	file_path = None
	file_name = None
	
	def __init__(self, file_name, project):
		self.project = project
		self.file_path = os.path.join(self.project.template_dir, file_name)
		self.file_name = os.path.basename(self.file_path)
		self.title = self.extract_title()
	
	def __eq__(self, template):
		if isinstance(template, Template):
			return self.file_name == template.file_name
		elif isinstance(template, str):
			return self.file_name == template
		else:
			return False
	
	def __hash__(self):
		return hash(self.file_name)
	
	def extract_title(self):
		if self.project.use_html_titles:
			with open(self.file_path) as f:
				s = re.search(r'<title>(.+?)</title>', f.read().decode(settings.FILE_CHARSET), re.MULTILINE)
				if s:
					return s.group(1)
		
		# Use file name as title
		return os.path.splitext(self.file_name)[0].replace("_", " ")