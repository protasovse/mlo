from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django_mysql.models import EnumField
from timezone_field import TimeZoneField

from apps.entry.models import Question
from config.settings import AUTH_USER_MODEL

ADVICE_NEW = 'new'
ADVICE_PAID = 'paid'
ADVICE_INWORK = 'inwork'
ADVICE_ANSWERED = 'answered'
ADVICE_CLOSED = 'closed'
ADVICE_CANCELED = 'canceled'

ADVICE_STATUSES = [
      (ADVICE_NEW, 'Новая'),
      (ADVICE_PAID, 'Оплачена'),
      (ADVICE_INWORK, 'В работе'),
      (ADVICE_ANSWERED, 'Есть ответ'),
      (ADVICE_CLOSED, 'Завершена'),
      (ADVICE_CANCELED, 'Отменена'),
    ]


class Advice(models.Model):
    """
    Платные консультации.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.NOT_PROVIDED,
        related_name='advice'
    )

    expert = models.ForeignKey(
        AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.NOT_PROVIDED,
        verbose_name=_('Эксперт'),
    )

    status = EnumField(
        _('Статус'), db_index=True,
        choices=ADVICE_STATUSES, default=ADVICE_NEW)

    cost = models.PositiveIntegerField(_('Цена консультации'))

    class Meta:
        verbose_name = _('Платная консультация')
        verbose_name_plural = _('Платные консультации')

    # Оплачена, если состояние не равно 'new'
    @property
    def is_paid(self):
        return self.status != ADVICE_NEW

    # Переводим заявку в статус «Оплачено»
    def to_paid(self):
        if self.status == ADVICE_NEW:
            self.status = ADVICE_PAID
            self.save(update_fields=['status'])
            self.question.is_pay = True
            self.question.save(update_fields=['is_pay'])
            return True
        return False

    # Переводим заявку в статус «В работе», если есть user_id, то назначаем эксперта
    def to_in_work(self, user_id=None):
        if self.is_paid:
            if user_id is not None:
                self.expert_id = user_id
            self.status = ADVICE_INWORK
            self.save(update_fields=['is_pay', 'expert_id'])
            return True
        return False

    # Переводим заявку в статус «Ответ юриста»
    def to_answered(self):
        if self.status == ADVICE_ANSWERED:
            return True
        if self.status == ADVICE_INWORK:
            self.status = ADVICE_ANSWERED
            self.save(update_fields=['status'])
            return True
        return False

    # Переводим заявку в статус «Завершено»
    def to_closed(self):
        if self.status == ADVICE_ANSWERED:
            self.status = ADVICE_CLOSED
            self.save(update_fields=['status'])
            return True
        return False

    def __str__(self):
        return self.question.__str__()


class StatusLog(models.Model):
    """
    Журнал состояний консультаций
    """
    advice = models.ForeignKey(Advice, on_delete=models.CASCADE)

    status = EnumField(
        _('Статус'), db_index=True,
        choices=ADVICE_STATUSES)

    date = models.DateTimeField(
        _('Дата принятия состояния'),
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = _('Журнал состояний')
        verbose_name_plural = _('Журнал состояний')

    def __str__(self):
        return '%s (%s)' % (self.status, self.date)


class Queue(models.Model):
    """
    Очередь экспертов для оказания консультации
    """
    expert = models.ForeignKey(
        AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.NOT_PROVIDED,
        verbose_name=_('Эксперт'),
    )

    order = models.PositiveIntegerField(_('Порядок в очереди'))

    is_active = models.BooleanField(_('Активность эксперта в очереди'))

    class Meta:
        ordering = ('order',)
        verbose_name = _('Очередь экспертов')
        verbose_name_plural = _('Очередь экспертов')


def update_expert_in_queue(user_id):
    """
    Здесь нужно проверить условия, может ли пользователь быть в очереди и обновить его активность.

    1. Пользователь есть в модели Expert, то

        1. Если пользователя нет в модели Scheduler, то
                Добавить со значениями по умолчанию

        2. Если пользователя нет в модели Queue, то
                Добавить с order = max(order)+1 и is_active=True
                можно return is_active

        3. Если текущая дата попадает в промежуток из модели Scheduler, то
                Queue.is_active=True
            иначе
                Queue.is_active=False

        return is_active

    иначе

        1. Если пользователь есть в модели Queue, то
            Queue.is_active=False

        return False
    """
    user = get_user_model().object.get(pk=user_id)


class Expert(models.Model):
    # Эксперты. Является ли на данный момент пользователь экспертом
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.NOT_PROVIDED,
    )

    class Meta:
        verbose_name = _('Эксперт')
        verbose_name_plural = _('Эксперты')

    def __str__(self):
        return self.user


class Scheduler(models.Model):
    """
    Планировщик рабочего дня
    """
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.NOT_PROVIDED,
    )

    timezone = TimeZoneField(
        default='Europe/Moscow',
        verbose_name=_('Временная зона'),
    )

    begin = models.TimeField(
        verbose_name=_('Начало рабочего дня'),
        default='00:00:00',
        help_text=_('Пожалуйста, вводите время по МСК.'),
    )

    end = models.TimeField(
        verbose_name=_('Конец рабочего дня'),
        default='23:59:59',
        help_text=_('Пожалуйста, вводите время по МСК.'),
    )

    all_time = models.BooleanField(
        default=True,
        verbose_name=_('Принимать заявки 24 часа'),
        help_text=_('Если не хотите принимать заявки круглосуточно, то снимите флажок и установите рабочий'
                    ' временной промежуток. Заявки будут приходить только в это время.'),
    )

    weekend = models.BooleanField(
        default=True,
        verbose_name=_('Принимать заявки в выходные дни'),
        help_text=_('Если не хотите принимать заявки в выходные дни (суббота, воскресенье), то снимите флажок.'),
    )

    def __str__(self):
        time = '24 часа' if self.all_time else 'с %s до %s' % (self.begin, self.end)
        return '%s (%s мск.)' % (self.user, time)


def add_status_log_receiver(sender, instance, *args, **kwargs):
    """
    Добавляем запись в журнал состояний при изменении состояния консультации
    """
    c = StatusLog.objects.create(advice=instance, status=instance.status)
    c.save()

post_save.connect(add_status_log_receiver, sender=Advice)