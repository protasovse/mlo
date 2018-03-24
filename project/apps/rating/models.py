from django.db import models

from django.utils.translation import ugettext_lazy as _

from apps.rating.settings import RATING_PERIOD
from config import settings
from config.settings import AUTH_USER_MODEL

'''
1	answer                  Ответ на вопрос	                                                2
2	usefull_answer_client	Полезный ответ на вопрос. Если нажал тот, кто задал вопрос.	    5
3	useless_answer_client	Бесполезный ответ на вопрос. Нажал тот, кто задал вопрос.	    -5
4	usefull_answer_lawyer	Полезный ответ на вопрос. Нажал другой юрист.	                3
5	useless_answer_lawyer	Бесполезный ответ на вопрос. Нажал другой юрист.	            -3
6	add_answer	            Дополнительный ответ или ответ на уточнение	                    1
'''


class Type(models.Model):
    """
    Типы баллов рейтинга.
    Здесь описываются типы балла: за что присваивается, ключ, значение
    """
    key = models.CharField(
        _('Ключ'),
        max_length=128,
    )

    value = models.SmallIntegerField(
        _('Балл'),
    )

    description = models.CharField(
        _('Описание'),
        max_length=255,
    )

    class Meta:
        verbose_name = _('Тип баллов')
        verbose_name_plural = _('Типы баллов')

    def __str__(self):
        return '%s (%d)' % (self.description, self.value)


class RatingScore(models.Model):
    """
    Баллы рейтинга пользователей.
    Здесь сохраняем каждый балл с комментарием, за что присвоен.
    """
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь')
    )

    type = models.ForeignKey(
        Type,
        on_delete=models.NOT_PROVIDED,
        verbose_name=_('Тип балла')
    )

    date = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name=_('Дата'),
    )

    class Meta:
        verbose_name = _('Балл')
        verbose_name_plural = _('Баллы')

    def save(self, *args, **kwargs):
        self.value = self.type.value
        return super(RatingScore, self).save(*args, **kwargs)

    def __str__(self):
        return '%s: %s (%s) — %d' % (self.user, self.type.key, self.date, self.type.value)


class RatingScoreComment(models.Model):
    """
    Комментарии, за что начислен балл
    """
    rating_score = models.OneToOneField(
        RatingScore,
        on_delete=models.CASCADE,
        related_name='comment',
    )

    comment = models.CharField(
        null=True,
        blank=True,
        max_length=128,
    )


class Rating(models.Model):
    """
    Рейтинг — суммы баллов
    """
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rating',
        verbose_name=_('Пользователь'),
        primary_key=True,
    )

    day_rate = models.IntegerField(
        _('Рейтинг за сутки'),
        db_index=True,
        default=0,
    )

    week_rate = models.IntegerField(
        _('Рейтинг за неделю'),
        db_index=True,
        default=0,
    )

    month_rate = models.IntegerField(
        _('Рейтинг за месяц'),
        db_index=True,
        default=0,
    )

    rate = models.IntegerField(
        _('Рейтинг за всё время'),
        db_index=True,
        default=0,
    )

    @property
    def get_rate(self):

        if RATING_PERIOD == 'day':
            return self.day_rate
        elif RATING_PERIOD == 'week':
            return self.week_rate
        elif RATING_PERIOD == 'month':
            return self.month_rate
        else:
            return self.rate

    class Meta:
        ordering = ('-{}_rate'.format(RATING_PERIOD), )
        verbose_name = _('Рейтинг')
        verbose_name_plural = _('Рейтинг')

    def __str__(self):
        return '%s: %d' % (self.user, self.get_rate)
