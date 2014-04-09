import os
import datetime

try:
    from settings_local import *
except ImportError:
    print u'File settings_local.py is not found. Please add it (with at least some database settings).'

# Django settings for opinion project.

# This is needed for "debug" to be accessible from a template
INTERNAL_IPS = (
    '127.0.0.1',
)

AUTHENTICATION_BACKENDS = (
    'opinion.code-auth.EntryCodeModelBackend',
    'opinion.email-auth.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

ADMINS = (
    ('Hybrid Wisdom Support', 'support@hybridwisdom.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# The site is the first (only) site in the database
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'minidetector.Middleware'
    #'opinion.tracking.middleware.VisitorTrackingMiddleware'
)

ROOT_URLCONF = 'opinion.urls'

TEMPLATE_DIRS = (
    # Found in Django Book:
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
    
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
"opinion.context_processors.url_root",
"opinion.context_processors.entry_codes",
"opinion.context_processors.assets_url",
"django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'opinion.opinion_core',
    'opinion.registration',
    #'opinion.tracking',
	#'opinion.django_evolution'
)

# Maximum length of comments for a user's ratings
MAX_COMMENT_LENGTH = 1000

# Max and min values for user ratings on statements and comments
MIN_RATING = 0.0
MAX_RATING = 1.0

# Registration settings
ACCOUNT_ACTIVATION_DAYS = 30

# Recaptcha keys
RECAPTCHA_PUB_KEY = "6LeieAgAAAAAANZwoiLY4sULlQCCvcincBC8UPT"
RECAPTCHA_PRIVATE_KEY = "6LeieAgAAAAAAEEPZSaGm8xnUjVUT7eUJkKwVJ5n"

# ID used for logging
OS_ID_DEFAULT = 1

#if DATABASE_ENGINE == 'mysql':
#  DATABASE_OPTIONS = {"init_command": "SET storage_engine=INNODB"}

#read geojson locally
GEOJSON_ROOT = os.path.abspath(os.path.dirname(__file__))
