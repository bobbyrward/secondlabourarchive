# Django settings for djangotest project.

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('null', 'hash.bang.bin.bash@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'hydra'
DATABASE_USER = 'null'
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = False

MEDIA_ROOT = '/home/null/src/comicsarchive/media'
MEDIA_URL = 'http://secondlabourarchive.info/media/'
ADMIN_MEDIA_PREFIX = '/admin_media/'


LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'null'
DEFAULT_FROM_EMAIL = 'Second Labour Archive <null@secondlabourarchive.info>'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'aqj_j9x_(03)2^go4es_jys@ge=om(d5qmtyxi!z)8@24^41-a'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'comicsarchive.urls'

TEMPLATE_DIRS = (
    "/home/null/src/comicsarchive/templates",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'comicsarchive.archive',
    'registration',
    'django.contrib.humanize',
)
