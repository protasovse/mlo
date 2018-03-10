from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ReviewConfig(AppConfig):
    name = 'apps.review'
    verbose_name = _('Лайки и отзывы на ответы')
