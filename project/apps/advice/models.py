from datetime import timedelta

from django.db import models
from django.utils import timezone
from django_mysql.models import EnumField
from timezone_field import TimeZoneField

from django.utils.translation import ugettext_lazy as _

from apps.advice.setting import ADVICE_COST
from . import emails
from apps.entry.models import Question
from config.settings import AUTH_USER_MODEL

ADVICE_NEW = 'new'
ADVICE_PAID = 'paid'
ADVICE_INWORK = 'inwork'
ADVICE_ANSWERED = 'answered'
ADVICE_ADDQUESTION = 'addquestion'
ADVICE_CLOSED = 'closed'
ADVICE_CANCELED = 'canceled'

ADVICE_STATUSES = [
      (ADVICE_NEW, 'Новая'),
      (ADVICE_PAID, 'Оплачена'),
      (ADVICE_INWORK, 'В работе'),
      (ADVICE_ANSWERED, 'Ответ эксперта'),
      (ADVICE_ADDQUESTION, 'Дополнительный вопрос'),
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

    cost = models.PositiveIntegerField(
        default=ADVICE_COST,
        verbose_name=_('Цена консультации'),
    )

    payment_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Дата поступления оплаты'),
    )

    answered_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Дата ответа'),
        help_text=_('Когда эксперт подготовит консультацию')
    )

    class Meta:
        verbose_name = _('Платная консультация')
        verbose_name_plural = _('Платные консультации')

    # Оплачена, если состояние не равно 'new'
    @property
    def is_paid(self):
        return self.status != ADVICE_NEW

    # Переводим заявку в статус «Оплачено», назначаем эксперта из очереди
    def to_paid(self):
        if self.status in (ADVICE_NEW, ADVICE_PAID):
            self.status = ADVICE_PAID
            from apps.advice.utils import queue_get_first
            expert = queue_get_first()  # получаем текущего пользователя и смещаем очередь
            self.expert = expert
            self.payment_date = timezone.now()
            self.save(update_fields=['expert', 'status', 'payment_date'])
            # Уведомляем эксперта о назначении заявки
            emails.send_advice_appoint_expert_email(self)
            return True
        return False

    # Переводим заявку в статус «В работе»
    # (num_hours — через сколько часов эксперт обещает дать ответ)
    def to_in_work(self, num_hours):
        if self.is_paid:
            self.status = ADVICE_INWORK
            self.answered_date = timezone.now() + timedelta(hours=num_hours)
            self.save(update_fields=['status', 'answered_date'])
            # Уведомляем клиента о новом назначении эксперта
            return True
        return False

    # Переводим заявку в статус «Ответ эксперта»
    def to_answered(self):
        if self.status in (ADVICE_ADDQUESTION, ADVICE_INWORK):
            self.status = ADVICE_ANSWERED
            self.save(update_fields=['status'])
            # Уведомляем клиента о новом ответе
            return True
        return False

    # Переводим заявку в статус «Дополнительный вопрос»
    def to_addquestion(self):
        if self.status in (ADVICE_ANSWERED, ADVICE_INWORK):
            self.status = ADVICE_ADDQUESTION
            self.save(update_fields=['status'])
            # Уведомляем эксперта о дополнительном вопросе
            return True
        return False

    # Переводим заявку в статус «Завершено»
    def to_closed(self):
        if self.status == ADVICE_ANSWERED:
            self.status = ADVICE_CLOSED
            self.save(update_fields=['status'])
            # Уведомляем эксперта о завершении консультации и переводе денег на счёт
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

    def __str__(self):
        return '%s - %d - %s' % (self.expert, self.order, self.is_active)


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
        return self.user.__str__()


class Scheduler(models.Model):
    """
    Планировщик рабочего дня
    """
    expert = models.OneToOneField(
        AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.NOT_PROVIDED,
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name=_('Принимать заявки'),
        help_text=_('Я готов принимать заявки на платные консультации.'),
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

    weekend = models.BooleanField(
        default=True,
        verbose_name=_('Принимать заявки в выходные дни'),
        help_text=_('Если не хотите принимать заявки в выходные дни (суббота, воскресенье), то снимите флажок.'),
    )

    def __str__(self):
        time = 'с %s до %s' % (self.begin, self.end)
        return '%s (%s мск.)' % (self.expert, time)
