from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MloAuthConfig(AppConfig):
    name = 'apps.mlo_auth'
    verbose_name = _('Пользователи')

