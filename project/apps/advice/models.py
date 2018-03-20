from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django_mysql.models import EnumField

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


def add_status_log_receiver(sender, instance, *args, **kwargs):
    """
    Добавляем запись в журнал состояний при изменении состояния консультации
    """
    c = StatusLog.objects.create(advice=instance, status=instance.status)
    c.save()

post_save.connect(add_status_log_receiver, sender=Advice)