""" Рубрики """

import re

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mptt.fields import TreeForeignKey, TreeManyToManyField
from mptt.models import MPTTModel


class Rubric(MPTTModel):

    name = models.CharField(_('Название'), max_length=128, unique=True)
    description = models.TextField(_('Описание рубрики'), blank=True)
    slug = models.CharField(max_length=128, unique=True, blank=True, verbose_name=_('Слаг'),
                            help_text=_('Можно не вводить. Автоматически генерируется из названия рубрики.'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            verbose_name=_('Родительская рубрика'), on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ('-id',)

    class Meta:
        ordering = ('level', 'name',)
        verbose_name = _('Рубрика')
        verbose_name_plural = _('Рубрики')

    @property
    def title_for_admin(self):
        return self.__str__()

    def get_absolute_url(self):
        return reverse('rubrics:rubric-detail', kwargs={'slug': self.slug})

    def _set_slug(self):
        """
        Устанавливает slug перед записью рубрики в бд
        """
        if self.slug == '':
            self.slug = re.sub(r'([^\w\d]|[\s])+', '-', self.name.strip().lower())[:128]

    def save(self, *args, **kwargs):
        self._set_slug()
        # Первую букву в верхний регистр
        self.name = self.name[0].upper() + self.name[1:]
        super(Rubric, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
        # return "%s (%d)" % (self.name, self.pk,)


class Classified(models.Model):

    rubrics = TreeManyToManyField(Rubric, blank=True, verbose_name=_('Рубрика'))

    class Meta:
        abstract = True
