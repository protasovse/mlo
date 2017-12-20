import os
import environ
from easy_thumbnails.conf import Settings as thumbnail_settings

root = environ.Path(__file__) - 3
env = environ.Env(DEBUG=(bool, False),)  # set default values and casting
environ.Env.read_env(root('.env'))

BASE_DIR = root()
PROJECT_DIR = environ.Path()
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

STATIC_ROOT = environ.Path('staticfiles').__str__()
STATICFILES_DIRS = [
    environ.Path('media/vue/bundles').__str__(),
    environ.Path('static').__str__(),
]

STATIC_URL = '/static/'

ALLOWED_HOSTS = [
    '127.0.0.1'
]

MEDIA_ROOT = environ.Path('storage').__str__()
MEDIA_URL = '/storage/'

if DEBUG:
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
    'django_mptt_admin',
    'rest_framework',
    'easy_thumbnails',
    'easy_select2',
    'django_select2',
    'image_cropping',
    # 'vk_cities',
    'apps.mlo_auth',
    'apps.entry',
    'apps.rubric',
    'apps.account',
    'apps.svem_auth',
    'apps.svem_system',
    'apps.sxgeo',
]

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_CONFIG = env.email_url('EMAIL_URL', backend=EMAIL_BACKEND)
vars().update(EMAIL_CONFIG)


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
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [environ.Path('templates').__str__()],
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
SITE_PROTOCOL = 'https'


VK_CLIENT_ID = 6302697
VK_CLIENT_SECRET = 'iu1QGd2VbzQMKSi5AxaP'
VK_REDIRECT_URL = 'https://мойюрист.онлайн/auth/vk'

FB_CLIENT_ID = 150974185544797
FB_CLIENT_SECRET = '6e13e4e659064e7fbbc65c30c8ce0c5c'
FB_REDIRECT_URL = 'https://мойюрист.онлайн/auth/fb'
