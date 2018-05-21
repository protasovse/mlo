import os
import environ
import locale
from easy_thumbnails.conf import Settings as thumbnail_settings


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


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
    '85.143.174.106'
]


MEDIA_ROOT = environ.Path('storage').__str__()
MEDIA_URL = '/storage/'

DATA_DIR = PROJECT_DIR + '/media'+'/data/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'django_mptt_admin',
    'easy_thumbnails',
    'django_select2',
    'django_mysql',
    'phonenumber_field',
    'timezone_field',
    'image_cropping',
    'pagedown',
    'bootstrap4',
    'dbmail',
    'debug_toolbar',

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
    'apps.article',
]

SITE_ID = env('SITE_ID')
SITE_URL = env('SITE_URL')
SITE_PROTOCOL = env('PROTOCOL')
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
    'apps.sxgeo.middleware.loc.LocationIdentify',
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
                "config.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

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

THUMBNAIL_PROCESSORS = ('image_cropping.thumbnail_processors.crop_corners',) + thumbnail_settings.THUMBNAIL_PROCESSORS

APPEND_SLASH = True

VK_CLIENT_ID = 3344860
VK_CLIENT_SECRET = 'idSIuk1OKdxZRxQrDrTC'
VK_REDIRECT_URL = 'http://xn--h1abiilhh6g.xn--80asehdb:8000/auth/vk'

FB_CLIENT_ID = 1422542761187900
FB_CLIENT_SECRET = 'ddd3cae70cb3abb564c704731d79bdb7'
FB_REDIRECT_URL = 'http://127.0.0.1:8000/auth/fb'


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10*1024*1024

INTERNAL_IPS = ['127.0.0.1']

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_CONFIG = env.email_url('EMAIL_URL', backend=EMAIL_BACKEND)
vars().update(EMAIL_CONFIG)

DATABASES = {'default': env.db()}

IQSMS_API_LOGIN = "z1522654896889"
IQSMS_API_PASSWORD = "972276"
IQSMS_FROM = "YURIST24"
IQSMS_URL = "http://api.iqsms.ru/messages/v2/send/"


GOOGLE_HORT_API_URL = 'https://www.googleapis.com/urlshortener/v1/url'
GOOGLE_HORT_API_KEY = 'AIzaSyD7GJizTAQaQ3C0v_ysFTJz2HWZMopHb5E'

HOT_LINE_PHONES = {
    'Московская область': '8 (495) 568-24-78',
    'Москва': '8 (495) 568-24-78',
    'Санкт-Петербург': '8 (812) 458-04-71',
    'Ленинградская область': '8 (812) 458-04-71',
    'остальные': None
}


# Платёжная информация об money.yandex аккаунте
MONEY_YANDEX_SECRET = 'bhpC6s2sVFnJQF8l/b3K9nV0'

# Номер кошелька для оплаты
MONEY_YANDEX_PURSE = 410014165217866

PAYMENT_FORM_TITLE = "Мойюрист.онлайн — юридическая консультация онлайн"
PAYMENT_FORM_TARGET = "Услуга «Персональный юрист». Вопрос №"

# Стоимость консультации
ADVICE_COST = 5  # руб.

# Время через которое заявка переходит следующему по очереди
ADVICE_OVERDUE_TIME = 30  # min

# Гонорар эксперта в процентах
ADVICE_EXPERT_FEE_IN_PERCENT = 55  # %

ANSWERS_TREE_IS_EXPANDED = True

ALL_PARTNER = False  # Партнёрска программа
# URL для обработки заявок с виджета: /widget_send