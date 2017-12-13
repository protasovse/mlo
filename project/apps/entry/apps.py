from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EntryConfig(AppConfig):
    name = 'apps.entry'
    verbose_name = _('Вопросы, ответы и статьи')

