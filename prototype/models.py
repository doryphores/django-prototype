import os
import re
import logging
import json
from prototype import utils
from django.conf import settings
from prototype.utils import make_tls_property

logger = logging.getLogger(__name__)


CURRENT_PROJECT = make_tls_property()


def get_projects():
	"""
	Retrieves list of projects
	"""
	pass


class Project(object):
	defaults = {
		'use_html_titles': False,
		'toolbar_position': 'top',
		'data_folder': 'data',
	}

	def __init__(self, config):
		self.defaults.update(config)
		self.name = self.defaults['name']
		self.slug = self.defaults['slug']
		self.data_folder = self.defaults['data_folder']
		self.use_html_titles = self.defaults['use_html_titles']
		self.toolbar_position = self.defaults['toolbar_position']
		self.templates_root = os.path.realpath(os.path.join(settings.PROTOTYPE_PROJECTS_ROOT, self.slug))
		self.data_root = os.path.join(settings.PROTOTYPE_PROJECTS_ROOT, self.slug, self.data_folder)

		self.refresh()

	def get_absolute_url(self):
		"""
		Returns absolute URL to project
		"""
		return 'http://%s.%s' % (self.slug, settings.PROTOTYPE_PROJECTS_HOST)

	def refresh(self):
		"""
		Refreshes template and data collections
		To be run once for each request
		See get_current in ProjectManager above
		"""

		# Read and parse templates and data files
		self._templates = TemplateCollection(self)
		self._data = DataDict(self)

	@property
	def templates(self):
		if not self._templates:
			self.refresh()
		return self._templates

	@property
	def data(self):
		if not self._data:
			self.refresh()
		return self._data

	def __unicode__(self):
		return u'%s' % self.name


class DataDict(dict):
	"""
	A custom dict object for storing mocking data structures for a project

	It handles the parsing of JSON files and stores them
	"""
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


class TemplateCollection(list):
	"""
	Iterable collection of templates
	Also holds last modified timestamp and refresh mechanism to minimise file reads
	"""

	def __init__(self, project):
		self.project = project
		self.last_modified = None
		self.refresh()

	def refresh(self):
		# Get list of templates if modified
		file_list = utils.list_dir_if_changed(self.project.templates_root, self.last_modified, ["htm", "html"])

		if file_list:
			self[:] = [Template(file_name, self.project) for file_name in file_list[0]]
			self.last_modified = file_list[1]

			logger.debug('Reloaded template list for project %s' % self.project.name)


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
		self.slug = self.file_name.split('.')[0]
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
		return os.path.splitext(self.file_name)[0].replace("_", " ").title()
