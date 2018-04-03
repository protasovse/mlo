import os
import environ
from easy_thumbnails.conf import Settings as thumbnail_settings

root = environ.Path(__file__) - 3
env = environ.Env(DEBUG=(bool, False), )  # set default values and casting
environ.Env.read_env(root('.env'))

BASE_DIR = root()

PROJECT_DIR = BASE_DIR + '/project'

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

STATIC_ROOT = environ.Path('staticfiles').__str__()
STATICFILES_DIRS = [
    PROJECT_DIR + '/media/vue/bundles',
    PROJECT_DIR + '/static',
]

STATIC_URL = '/static/'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'мойюрист.онлайн',
    'xn--h1abiilhh6g.xn--80asehdb',
]

MEDIA_ROOT = environ.Path('storage').__str__()
MEDIA_URL = '/storage/'

DATA_DIR = PROJECT_DIR + '/media'+'/data/'

if 0 and DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console'],
            }
        },
    }

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'haystack',
    'django_mptt_admin',
    'easy_thumbnails',
    'easy_select2',
    'django_select2',
    'django_mysql',
    'phonenumber_field',
    'timezone_field',
    'image_cropping',
    'apps.mlo_auth',
    'apps.entry',
    'apps.rubric',
    'apps.account',
    'apps.svem_auth',
    'apps.svem_system',
    'apps.sxgeo',
    'apps.front',
    'apps.question',
    'apps.review.apps.ReviewConfig',
    'apps.advice.apps.AdviceConfig',
    'apps.rating.apps.RatingConfig',
    'apps.billing.apps.BillingConfig',
    'dbmail',
    'debug_toolbar',
]

SITE_ID = env('SITE_ID')
AUTH_USER_MODEL = 'mlo_auth.user'
AUTHENTICATION_BACKENDS = ['apps.mlo_auth.models.Backend']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR + '/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {'default': env.db()}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'PAGE_SIZE': 10
}

THUMBNAIL_PROCESSORS = (
                           'image_cropping.thumbnail_processors.crop_corners',
                       ) + thumbnail_settings.THUMBNAIL_PROCESSORS

APPEND_SLASH = True
SITE_PROTOCOL = 'http'

VK_CLIENT_ID = 3344860
VK_CLIENT_SECRET = 'idSIuk1OKdxZRxQrDrTC'
VK_REDIRECT_URL = 'http://xn--h1abiilhh6g.xn--80asehdb:8000/auth/vk'

FB_CLIENT_ID = 1422542761187900
FB_CLIENT_SECRET = 'ddd3cae70cb3abb564c704731d79bdb7'
FB_REDIRECT_URL = 'http://127.0.0.1:8000/auth/fb'


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10*1024*1024

INTERNAL_IPS = ['127.0.0.1']

'''
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}
'''


EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_CONFIG = env.email_url('EMAIL_URL', backend=EMAIL_BACKEND)
vars().update(EMAIL_CONFIG)

# DB_MAILER iqsms.ru provider settings
# DB_MAILER_SMS_PROVIDER = 'dbmail.providers.smsbliss.sms'

# IQSMS_API_LOGIN = "z1522654896889"
# IQSMS_API_PASSWORD = "972276"
# IQSMS_FROM = "YURIST24"

# smsbliss.ru/
# SMSBLISS_API_URL = 'http://api.smsbliss.net/messages/v2/send.json'
# SMSBLISS_LOGIN = 'protasovse'
# SMSBLISS_PASSWORD = 'hui7586381'
# SMSBLISS_FROM = 'TEST'


ADVICE_COST = 800  # руб.