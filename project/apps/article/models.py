from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_mysql.models import EnumField

from apps.entry.managers import DELETED, PUBLISHED, BLOCKED, DRAFT
from apps.entry.models import Entry, Titled
from apps.rubric.models import Classified


class Dir(models.Model):
    """
    Разделы статей
    """
    name = models.CharField(_('Name'), max_length=128,
                            help_text=_('Название раздела'))

    description = models.TextField(_('Description'), help_text=_('Описание'),
                                   null=True, blank=True)

    slug = models.CharField(max_length=128, unique=True, verbose_name=_('Слаг'))

    class Meta:
        verbose_name = _("Раздел статей")
        verbose_name_plural = _("Разделы")


class Article(Entry, Titled, Classified):
    """
    Статьи
    """
    dir = models.ForeignKey(Dir, on_delete=models.PROTECT, default=None)

    status = EnumField(
        _("Статус"), db_index=True,
        choices=[DELETED, PUBLISHED, BLOCKED, DRAFT], default=PUBLISHED)

    class Meta:
        verbose_name = _("Статья")
        verbose_name_plural = _("Статьи")

