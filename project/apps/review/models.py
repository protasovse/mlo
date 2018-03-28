import misaka
from django.db import models, connection
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.entry.models import Entry
from apps.review.managers import ReviewManager, LikeManager
from config.settings import AUTH_USER_MODEL


class Likes(models.Model):
    """
    Лайки
    """
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='likes',
                              verbose_name=_('Ответ'))

    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_('Пользователь'),
                             help_text=_('Пользователь, который поставил отметку'), on_delete=models.CASCADE)

    date = models.DateTimeField(_('Дата'), default=timezone.now)

    value = models.SmallIntegerField(_('Балл'))

    objects = LikeManager()

    class Meta:
        unique_together = ('entry', 'user')
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

    @property
    def title_for_admin(self):
        return "Вопрос: %d" % (self.entry)

    def __str__(self):
        return "%d: %s (%d)" % (self.entry.pk, self.user.get_full_name, self.value)


class Review(models.Model):
    """
    Отзывы и комментарии к лайкам
    """
    like = models.OneToOneField(Likes, on_delete=models.CASCADE, related_name='review')
    review = models.TextField(_('Текст отзыва'))

    objects = ReviewManager()

    class Meta:
        ordering = ('-id', )
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

    @property
    def html_review(self):
        """
        Возвращает текст отзыва форматированное в HTML.
        """
        return misaka.html(self.review)

    def __str__(self):
        return self.review

