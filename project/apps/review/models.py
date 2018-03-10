from django.db import models, connection
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.entry.models import Entry
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

    class Meta:
        unique_together = ('entry', 'user')
        ordering = ('-date',)
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

    @property
    def title_for_admin(self):
        return "Вопрос: %d" % (self.entry.answer.on_question_id)

    def __str__(self):
        return "%d: %s (%d)" % (self.entry.pk, self.user.get_full_name, self.value)


class Review(models.Model):
    """
    Отзывы и комментарии к лайкам
    """
    like = models.OneToOneField(Likes, on_delete=models.CASCADE, related_name='review')
    review = models.TextField(_('Текст отзыва'))

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

    def __str__(self):
        return self.review


def post_save_like_receiver(sender, instance, *args, **kwargs):
    """
    Добавление или удаление лайка. Считаем суммы баллов и кешируем в entry.like_count
    """
    cursor = connection.cursor()
    cursor.execute("""
      UPDATE entry_entry SET entry_entry.like_count = 
        (SELECT SUM(value) FROM entry_likes WHERE entry_id = '%s')
      WHERE id = '%s' LIMIT 1
    """, [instance.entry.pk, instance.entry.pk])

post_save.connect(post_save_like_receiver, sender=Likes)
post_delete.connect(post_save_like_receiver, sender=Likes)