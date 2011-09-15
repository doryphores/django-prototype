import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

# Django settings for Prototype project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DEBUG_TOOLBAR_CONFIG = {
	'INTERCEPT_REDIRECTS': False,
}

INTERNAL_IPS=('127.0.0.1',)

ADMINS = (
	('Martin', 'martin.laine@gmail.com'),
)

SERVER_EMAIL = 'martin.laine@gmail.com'

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': os.path.join(PROJECT_PATH, "data", "db.sqlite"),					  # Or path to database file if using sqlite3.
		'USER': '',					  # Not used with sqlite3.
		'PASSWORD': '',				  # Not used with sqlite3.
		'HOST': '',					  # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',					  # Set to empty string for default. Not used with sqlite3.
	}
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

STATIC_ROOT = os.path.join(PROJECT_PATH, "public", "static")

STATIC_URL = '/__proto__/static/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "public", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/__proto__/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hhh$-&#y=#njlyz%%m)h=+qykef=6ce!2fmp^jzmyal3+e8qex'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'prototype.loaders.Loader',
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#	 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'prototype.middleware.RequestMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.request',
	'prototype.context_processors.data',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'south',
	'prototype',
)

# Cache config

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': '127.0.0.1:11211',
	}
}

#Loging configuration

LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'formatters': {
		'standard': {
			'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
		},
	},
	'handlers': {
		'default': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': os.path.join(PROJECT_PATH, 'logs', 'django.log'),
			'maxBytes': 1024*1024*5, # 5 MB
			'backupCount': 5,
			'formatter': 'standard',
		},
		'request_handler': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': os.path.join(PROJECT_PATH, 'logs', 'django_request.log'),
			'maxBytes': 1024*1024*5, # 5 MB
			'backupCount': 5,
			'formatter': 'standard',
		},
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler',
		}
	},
	'loggers': {
		'': {
			'handlers': ['default'],
			'level': 'DEBUG',
			'propagate': True
		},
		'django.db.backends': { # Stop SQL debug from logging to main logger
			'handlers': ['request_handler'],
			'level': 'DEBUG',
			'propagate': False
		},
	}
}

# Django prototype settings

PROTOTYPE_PROJECTS_ROOT = 'C:\\WebRoot\\templates'

PROTOTYPE_TEMPLATES_PATH = 'www'

PROTOTYPE_DEFAULT_DATA_PATH = 'data'

PROTOTYPE_PROJECTS_HOST = 'proto.local'

PROTOTYPE_BUILD_PATH = os.path.join(PROJECT_PATH, "data", "build")


try:
	import local_settings
except ImportError:
	pass
else:
	# Import any symbols that begin with A-Z. Append to lists any symbols that
	# begin with "EXTRA_".
	import re
	for attr in dir(local_settings):
		match = re.search('^EXTRA_(\w+)', attr)
		if match:
			name = match.group(1)
			value = getattr(local_settings, attr)
			try:
				globals()[name] += value
			except KeyError:
				globals()[name] = value
		elif re.search('^[A-Z]', attr):
			globals()[attr] = getattr(local_settings, attr)