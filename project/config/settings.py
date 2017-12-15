import os
import environ

root = environ.Path(__file__) - 3
env = environ.Env(DEBUG=(bool, False),)  # set default values and casting
environ.Env.read_env(root('.env'))

BASE_DIR = root()
PROJECT_DIR = environ.Path()
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')


STATIC_ROOT = environ.Path('project/static').__str__()
STATICFILES_DIRS = [
   environ.Path('project/media/vue/bundles').__str__()
]

ALLOWED_HOSTS = [
    '127.0.0.1'
]


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
    'easy_select2',
    'apps.mlo_auth',
    'apps.entry',
    'apps.rubric',
    'apps.svem_auth',
]

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_CONFIG = env.email_url('EMAIL_URL', backend=EMAIL_BACKEND)
vars().update(EMAIL_CONFIG)


SITE_ID = env('SITE_ID')
AUTH_USER_MODEL = 'mlo_auth.user'

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
        'DIRS': [environ.Path('project/templates').__str__()],
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'PAGE_SIZE': 10
}

FIXTURE_DIRS = (
   'apps/rubric/fixtures/initial.json',
   'apps/entry/fixtures/initial.json',
)
