import os, sys, site

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(PROJECT_ROOT)

if os.name == 'nt':
    site.addsitedir(os.path.join(PROJECT_ROOT, '.env/Lib/site-packages'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

if os.name == 'nt':
	import monitor
	monitor.start(interval=1.0)