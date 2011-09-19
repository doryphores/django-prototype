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
		"""
		
		project_slug = ""
		
		# Extract project slug from host name (the first bit)
		m = re.match(r'([^\.]+)\.%s' % settings.PROTOTYPE_PROJECTS_HOST, request.get_host())
		if m:
			project_slug = m.group(1)
		
		try:
			current_project = self.get(slug=project_slug)
			current_project.refresh()
		except Project.DoesNotExist:
			return None
		
		return current_project

class Project(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	
	data_folder = models.CharField(max_length=255, blank=True, default=settings.PROTOTYPE_DEFAULT_DATA_PATH, help_text="The folder within the project where mocking data files are stored")
	static_root = models.CharField(max_length=255, blank=True, default="static", help_text="The folder within the template root where static assets are stored")
	
	use_html_titles = models.BooleanField(default=True, verbose_name='Titles', help_text="Which method to use to display template titles")
	
	objects = ProjectManager()
	
	def get_absolute_url(self):
		"""
		Returns absolute URL to project
		"""
		return 'http://%s.%s' % (self.slug, settings.PROTOTYPE_PROJECTS_HOST)
	
	@property
	def templates_root(self):
		return os.path.join(settings.PROTOTYPE_PROJECTS_ROOT, self.slug, settings.PROTOTYPE_TEMPLATES_PATH)
	
	@property
	def data_root(self):
		return os.path.join(settings.PROTOTYPE_PROJECTS_ROOT, self.slug, self.data_folder)
	
	@property
	def build_root(self):
		return safe_join(settings.PROTOTYPE_BUILD_PATH, self.slug)
	
	def refresh(self):
		"""
		Refreshes template and data collections
		To be run once for each request
		See get_current in ProjectManager above
		"""
		
		cached_data = cache.get(self.slug, {})
		
		if not cached_data:
			self.templates = TemplateCollection(self)
			self.data = DataDict(self)
		else:
			self.templates = cached_data["templates"]
			self.templates.refresh()
			self.data = cached_data["data"]
			self.data.refresh()
		
		cache.set(self.slug, { 'templates': self.templates , 'data': self.data })
	
	def init_build(self):
		if os.path.isdir(self.build_root):
			rmtree(self.build_root)
	
	def prepare_css(self, file="screen.css"):
		# Prepare css
		css_dir = safe_join(self.templates_root, self.static_root, "css")
		p = re.compile('@import\s+"(.*?)".*', re.DOTALL)
		with open(safe_join(css_dir, file)) as screen_css:
			concat_css = screen_css.read().decode(settings.FILE_CHARSET)
			screen_css.seek(0)
			for line in screen_css:
				if line.find("@import") == 0:
					with open(safe_join(css_dir, p.sub(r'\1', line))) as f:
						concat_css = concat_css.replace(line, f.read().decode(settings.FILE_CHARSET))
		
		return cssmin.cssmin(concat_css)
	
	def build_static(self):
		self.init_build()
		
		asset_dir = safe_join(self.templates_root, self.static_root)
		
		# Copy all static assets
		copytree(asset_dir, self.build_root, ignore=ignore_patterns('.svn', 'images\\content'))
		
		# Concatenate and minify stylesheets to screen.min.css
		with codecs.open(safe_join(self.build_root, "css", "screen.min.css"), encoding='utf-8', mode='w+') as f:
			f.write(self.prepare_css())
		
		#build = (utils.zipdir(self.build_root), "build-%s.zip" % self.get_rev_number())
		
		path = 'builds/%s/build.zip' % self.slug
		
		if default_storage.exists(path):
			default_storage.delete(path)
		
		build = default_storage.save(path, ContentFile(utils.zipdir(self.build_root)))
		
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
		# If updating, ensure cached data is removed before saving
		if self.pk:
			old_slug = Project.objects.get(pk=self.pk).slug
			cache.delete(old_slug)
		super(Project, self).save(*args, **kwargs)
	
	def delete(self):
		# Removed cached data before deteting
		cache.delete(self.slug)
		super(Project, self).delete()
	
	def __unicode__(self):
		return u'%s' % self.name
	
	class Meta:
		ordering = ['name']

class DataDict(dict):
	def __init__(self, project):
		self.project = project
		self.last_modified = None
		self.refresh()
	
	def refresh(self):
		if os.path.isdir(self.project.data_root):
			file_list = utils.list_dir_if_changed(self.project.data_root, self.last_modified)
			
			if file_list:
				self.clear()
				
				for file_name in file_list[0]:
					file_parts = file_name.split(".")
					with open(os.path.join(self.project.data_root, file_name)) as f:
						try:
							self[file_parts[0]] = json.load(f)
						except:
							self[file_parts[0]] = None
				
				self.last_modified = file_list[1]
				
				logger.debug('Reloaded data store for project %s' % self.project.name)

class TemplateCollection(object):
	"""
	Iterable collection of templates
	Also holds last modified timestamp and refersh mechanism to minimise file reads
	"""
	
	def __init__(self, project):
		self.project = project
		self.collection = []
		self.index = -1
		self.last_modified = None
		self.refresh()
	
	def refresh(self):
		# Get list of templates if modified
		file_list = utils.list_dir_if_changed(self.project.templates_root, self.last_modified, ["htm", "html"])
		
		if file_list:
			self.collection = [Template(file_name, self.project) for file_name in file_list[0]]
			self.last_modified = file_list[1]
			
			logger.debug('Reloaded template list for project %s' % self.project.name)
	
	def __iter__(self):
		return self
	
	def next(self):
		self.index = self.index + 1
		if self.index == len(self.collection):
			self.index = -1
			raise StopIteration
		return self.collection[self.index]

class Template(object):
	"""
	For storing template data
	Knows how to extract titles from files
	Also contains logic for comparing to other templates
	so we can perform "if template in" operations 
	"""
	
	def __init__(self, file_name, project):
		self.project = project
		self.file_path = os.path.join(self.project.templates_root, file_name)
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