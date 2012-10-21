from django.conf import settings

from prototype.models import Project, CURRENT_PROJECT

import re
import os
import simplejson


class ProjectMiddleware(object):
	def process_request(self, request):
		m = re.match(r'([^\.]+)\.%s' % settings.PROTOTYPE_PROJECTS_HOST, request.get_host())
		config = {}
		config['slug'] = m.group(1)
		with open(os.path.join(settings.PROTOTYPE_PROJECTS_ROOT, config['slug'], 'prototype.json')) as f:
			config.update(simplejson.load(f))
			CURRENT_PROJECT.value = request.project = Project(config)
