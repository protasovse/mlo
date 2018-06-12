from datetime import timedelta

from django.db import models, transaction
from django.utils import timezone
from django_mysql.models import EnumField
from timezone_field import TimeZoneField

from django.utils.translation import ugettext_lazy as _

from apps.advice.manager import AdviceManager
from apps.entry.managers import DELETED, PUBLISHED
from . import emails
from apps.entry.models import Question
from config.settings import AUTH_USER_MODEL, ADVICE_COST, ADVICE_EXPERT_FEE_IN_PERCENT, ADVICE_OVERDUE_TIME

ADVICE_NEW = 'new'
ADVICE_PAID = 'paid'
ADVICE_PAYMENT_CONFIRMED = 'payment_confirmed'
ADVICE_INWORK = 'inwork'
ADVICE_ANSWERED = 'answered'
ADVICE_ADDQUESTION = 'addquestion'
ADVICE_CLOSED = 'closed'
ADVICE_CANCELED = 'canceled'

ADVICE_STATUSES = [
    (ADVICE_NEW, 'Новая'),
    (ADVICE_PAID, 'Оплачена'),
    (ADVICE_PAYMENT_CONFIRMED, 'Оплата подтверждена'),
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
    question = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
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

    overdue_date = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text=_('Время, когда заявка будет считаться просроченной и назначен новый эксперт'),
    )

    answered_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Дата ответа'),
        help_text=_('Когда эксперт подготовит консультацию')
    )

    objects = models.Manager()
    published = AdviceManager()

    class Meta:
        verbose_name = _('Платная консультация')
        verbose_name_plural = _('Платные консультации')

    # Назначить эксперта
    def appoint_expert(self):
        from apps.advice.utils import queue_get_first
        expert = queue_get_first()  # получаем текущего пользователя и смещаем очередь
        if expert:
            self.expert = expert
            self.overdue_date = timezone.now() + timedelta(minutes=ADVICE_OVERDUE_TIME)  # время просрочки
            self.save(update_fields=['expert', 'overdue_date'])
            # Уведомляем эксперта о назначении заявки
            emails.send_advice_appoint_expert_email(self)
            return True
        else:
            return False

    # Пользователь оплатил и перешёл на страницу вопроса
    def to_paid(self):
        # Если подтверждение платежа произошло быстрее чем, перевод в статус: ADVICE_NEW
        if self.status == ADVICE_PAYMENT_CONFIRMED:
            return True
        if self.status == ADVICE_NEW:
            self.status = ADVICE_PAID
            self.save(update_fields=['status'])
            return True
        return False

    # Переводим заявку в статус «Оплата подтверждена», назначаем эксперта из очереди
    # оплата подтверждается с помощью http уведомления: https://money.yandex.ru/myservices/online.xml
    # док: https://tech.yandex.ru/money/doc/dg/reference/notification-p2p-incoming-docpage/
    def to_payment_confirmed(self):
        if self.status in (ADVICE_NEW, ADVICE_PAID):
            with transaction.atomic():
                self.status = ADVICE_PAYMENT_CONFIRMED
                self.payment_date = timezone.now()
                self.save(update_fields=['status', 'payment_date'])
                self.question.status = PUBLISHED
                self.question.save(update_fields=['status'])
                self.appoint_expert()  # Назначаем эксперта
            return True
        return False

    # Переводим заявку в статус «В работе»
    # (num_hours — через сколько часов эксперт обещает дать ответ)
    def to_in_work(self, num_hours):
        if self.status == ADVICE_PAYMENT_CONFIRMED:
            with transaction.atomic():
                self.status = ADVICE_INWORK
                self.answered_date = timezone.now() + timedelta(hours=int(num_hours))
                self.save(update_fields=['status', 'answered_date'])
            # Уведомляем клиента о новом назначении эксперта
            emails.send_advice_to_in_work_to_client_message(self, num_hours)
            return True
        return False

    # Отказаться от заявки
    def to_refuse(self):
        if self.status == ADVICE_PAYMENT_CONFIRMED:
            with transaction.atomic():
                self.appoint_expert()
                return True
        return False

    # Переводим заявку в статус «Ответ эксперта»
    def to_answered(self):
        if self.status in (ADVICE_ADDQUESTION, ADVICE_INWORK):
            self.status = ADVICE_ANSWERED
            self.save(update_fields=['status'])
            # Уведомляем клиента о новом ответе
            emails.send_advice_new_answer(self)
            return True
        return False

    # Переводим заявку в статус «Дополнительный вопрос»
    def to_addquestion(self):
        if self.status in (ADVICE_ANSWERED, ADVICE_INWORK, ADVICE_ADDQUESTION):
            self.status = ADVICE_ADDQUESTION
            self.save(update_fields=['status'])
            # Уведомляем эксперта о дополнительном вопросе
            emails.send_advice_additional_question(self)
            return True
        return False

    # Переводим заявку в статус «Завершено»
    def to_closed(self):
        if self.status == ADVICE_ANSWERED:
            with transaction.atomic():
                self.status = ADVICE_CLOSED
                self.save(update_fields=['status'])
                from apps.billing.models import transfer_to_user
                transfer_to_user(self.expert, self.cost * ADVICE_EXPERT_FEE_IN_PERCENT / 100,
                                 'Гонорар за платный вопрос №{id}'.format(id=self.question_id))
            # Уведомляем эксперта о завершении консультации и переводе денег на счёт
            emails.send_advice_closed(self)
            return True
        return False

    # Переводим заявку в статус «Отменено»
    def to_canceled(self):
        if self.status != ADVICE_CLOSED:
            with transaction.atomic():
                self.status = ADVICE_CANCELED
                self.save(update_fields=['status'])
                self.question.status = DELETED
                self.question.save(update_fields=['status'])
            return True

    def get_public_data(self):
        return {
            'id': self.id,
            'status': self.status,
            'status_display': self.get_status_display(),
            'cost': self.cost,
            'expert': self.expert.get_public_data() if self.expert else False,
            'answered_date': self.answered_date.strftime('%d %B %Y %H:%M') if self.answered_date else False
        }


class StatusLog(models.Model):
    """
    Журнал состояний консультаций
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    status = EnumField(
        _('Статус'), db_index=True,
        choices=ADVICE_STATUSES)

    date = models.DateTimeField(
        _('Дата принятия состояния'),
        auto_now_add=True,
        editable=False
    )

    comment = models.CharField(
        _('Комментарий'),
        null=True,
        blank=True,
        max_length=255
    )

    class Meta:
        verbose_name = _('Журнал состояний')
        verbose_name_plural = _('Журнал состояний')


class Queue(models.Model):
    """
    Очередь экспертов для оказания консультации
    """
    expert = models.OneToOneField(
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
