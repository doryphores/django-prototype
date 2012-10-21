from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INSTALLED_APPS += ('debug_toolbar',)

DEBUG_TOOLBAR_CONFIG = {
	'INTERCEPT_REDIRECTS': False,
}
