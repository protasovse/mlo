""" Рубрики """

import re

import misaka
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mptt.fields import TreeForeignKey, TreeManyToManyField
from mptt.models import MPTTModel


class Rubric(MPTTModel):

    name = models.CharField(_('Name'), max_length=128,
                            help_text=_('Название рубрики'), unique=True)

    title = models.CharField(_('Title'), max_length=128,
                             help_text=_('Заголовок страницы'), blank=True)

    h1 = models.CharField(_('H1'), max_length=128,
                          help_text=_('Заголовок h1'), blank=True)

    link = models.CharField(_('Link'), max_length=128,
                            help_text=_('Текст для ссылок и навигации'), blank=True)

    call_to_action = models.CharField(_('Call to action'), max_length=128,
                                      help_text=_('Призыв к действию. Например: Проконсультаруйся с'
                                                  'жилищным юристом онлайн'), blank=True)

    advice_on = models.CharField(_('advice on'), max_length=128,
                                 help_text=_('Юристы и адвокаты проконсультируют … платно или бесплатно'), blank=True)

    description = models.TextField(_('Description'), help_text=_('Короткое описание'),
                                   null=True, blank=True)

    content = models.TextField(_('Content'), help_text=_('Содержание, статья'),
                               null=True, blank=True)

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

    @property
    def html_description(self):
        """
        Возвращает "description" форматированное в HTML.
        """
        return misaka.html(self.description)

    def get_absolute_url(self):
        if self.is_root_node():
            return reverse('questions:list_rubric',
                           kwargs={'rubric_slug': self.slug})
        else:
            return reverse('questions:list_subrubric',
                           kwargs={'subrubric_slug': self.slug, 'rubric_slug': self.get_root().slug, })

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
