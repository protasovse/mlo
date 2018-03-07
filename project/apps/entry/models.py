import misaka
from django.db import models, connection
from django.db.models.signals import post_save, pre_delete, post_delete
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.entry.managers import EntryPublishedManager, DELETED, DRAFT, PUBLISHED, AnswersManager
from apps.rubric.models import Classified
from config.settings import AUTH_USER_MODEL

CONSULT_COST = 800

STATUS_CHOICES = ((DELETED, _('Удалённый')),
                  (DRAFT, _('Черновик')),
                  (PUBLISHED, _('Опубликован')))

OFFER_NEW = '0'
OFFER_VIEWED = '1'
OFFER_PAID = '5'
OFFER_CANCELED = '-1'

OFFER_STATUS_CHOICES = ((OFFER_NEW, _('Новое')),
                        (OFFER_VIEWED, _('Просмотрено клиентом')),
                        (OFFER_PAID, _('Оплачен')),
                        (OFFER_CANCELED, _('Отменён')))


class Entry(models.Model):
    """
    Базовая модель записи. Все записи (вопросы, ответы, комментарии)
    будут наследовать свойства этой модели
    """

    content = models.TextField(_('Содержание'),)

    author = models.ForeignKey(
        AUTH_USER_MODEL,
        default=-1,
        related_name="%(class)s_set",
        on_delete=models.CASCADE,
        verbose_name=_('Автор')
    )

    pub_date = models.DateTimeField(
        _('Дата публикации'),
        db_index=True, default=timezone.now,
        editable=False
    )

    status = models.IntegerField(
        _('Статус'), db_index=True,
        choices=STATUS_CHOICES, default=PUBLISHED)

    like_count = models.IntegerField(
        _('Лайки'), db_index=True,
        default=0, editable=False
    )

    reply_count = models.IntegerField(
        _('Ответов'), db_index=True,
        default=0, editable=False)

    objects = models.Manager()
    published = EntryPublishedManager()

    def save(self, *args, **kwargs):
        return super(Entry, self).save(*args, **kwargs)

    def __str__(self):
        return "%d. %s " % (self.pk, self.content[:64])

    def __int__(self):
        return self.pk

    @property
    def html_content(self):
        """
        Возвращает "content" форматированное в HTML.
        """
        return misaka.html(self.content)

    # class Meta:
    #     abstract = True


class Files(models.Model):
    """
    Модель файлов, прикрепленных к записи.
    """
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='entries/%Y/%m/%d', verbose_name=_('Файл'))

    def get_basename(self):
        if self.file.name:
            import os
            return os.path.basename(self.file.name)

    class Meta:
        verbose_name = _('Файл')
        verbose_name_plural = _('Файлы')

    def __str__(self):
        return str(self.get_basename())


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
    like = models.OneToOneField(Likes, on_delete=models.CASCADE)
    review = models.TextField(_('Текст отзыва'))

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

    def __str__(self):
        return self.review


class Titled(models.Model):
    """
    Эту модель будут наследовать все совокупности записей,
    у которых кроме текстового содержания есть заголовок
    """
    title = models.CharField(blank=False, max_length=160, verbose_name=_('Заголовок'))

    class Meta:
        abstract = True


class Question(Entry, Titled, Classified):
    """
    Вопросы. Вопрос может задать и Клиент и Юрист. Для Клиента — это юридическая консультация.
    Для юриста — это обсуждение какой-либо сложной профессиональной ситуации.
    """

    # Вопрос платный если есть запись в таблице Consult, и вопрос оплачен
    is_pay = models.BooleanField(
        _('Платный вопрос'),
        default=False,
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = _("Вопрос")
        verbose_name_plural = _("Вопросы")

    def get_absolute_url(self):
        return reverse('questions:question-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '№%d. %s: (%s)' % (self.pk, self.title, self.get_status_display())


class Answer(Entry):
    """
    Ответы на вопросы. Ответ относится к определенному вопросу.
    Так же ответ может относиться к вопросу и другому ответу на этот вопрос, т.е. юрист может добавить только
    один ответ, который относится только к вопросу. Далее диалог между клиентом и юристом будет происходить
    «под» 1-м ответом юриста на вопрос.
    """
    # К какой записи (вопросу) относится, так же равна question.pk
    on_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_('На вопрос')
    )
    # Если является ответом на ответ, то содержит внешний ключ на этот ответ
    # parent — либо None, если ответ юриста первый, либо равен answer_id первого ответа.
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('К ответу'),
    )

    answers = AnswersManager()

    class Meta:
        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')

    def children(self):
        return Answer.answers.related_to_question(self.on_question_id).filter(parent=self)

    @property
    def is_parent(self):
        """
        Если True, то является первым ответом пользователя на вопрос
        """
        if self.parent_id is not None:
            return False
        return True

    def save(self, *args, **kwargs):
        if not hasattr(self, 'on_question'):
            self.on_question = self.parent.on_question
        return super(Answer, self).save()


class Offer(models.Model):
    """
    Предложение платных услуг юристом. Прикрепляется в ответе. В этом же ответе описывается суть предложения.
    """
    answer = models.OneToOneField(Answer,
                                  on_delete=models.CASCADE)

    cost = models.PositiveIntegerField(verbose_name=_('Стоимость услуг (₽)'))

    pub_date = models.DateTimeField(default=timezone.now)

    # Оплачена ли услуга автором вопроса, на который дан ответ с предложениями
    status = models.IntegerField(
        _('Статус счёта'), db_index=True,
        choices=OFFER_STATUS_CHOICES, default=OFFER_NEW)

    paid_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Счёт на оказание платных услуг"
        verbose_name_plural = "Счёта"

    def __str__(self):
        return "%d. стоимость: %d₽. (ответ %d, вопрос %d)" % \
               (self.pk, self.cost, self.answer.id, self.answer.on_question.id)


class ConsultState(models.Model):
    """
    Наименование состояний платной консультации:
    1. Новая (new) — вопрос задан и ещё не оплачен. (Статус по умолчанию для нового вопроса консультации)
    2. Оплачена (paid) — вопрос оплачен.
    2. В работе (inwork) — распределён эксперту и находится в работе.
    3. Ответ эксперта (answered) — эксперт ответил на вопрос. Далее, если клиент задаёт дополнительный вопрос,
       то вопрос переходит в статус «В работе», иначе клиент может либо закрыть вопрос, нажав на кнопку «Закрыть»,
       либо вопрос закрывается автоматически через 3 дня.
    4. Закрыт (closed) — вопрос закрыт. Расчёт произведён.
    """
    key = models.CharField(_('Название на латинице'), max_length=24)
    state = models.CharField(_('Название состояния'), max_length=24)

    class Meta:
        verbose_name = _('Платные консультации: таблица состояний')
        verbose_name_plural = _('Платные консультации: таблица состояний')

    def __str__(self):
        return self.state


class Consult(models.Model):
    """
    Платные консультации.
    Экспертов может быть несколько.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.NOT_PROVIDED,
        related_name='consult'
    )

    expert = models.ForeignKey(
        AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.NOT_PROVIDED,
        verbose_name=_('Эксперт'),
    )

    state = models.ForeignKey(
        ConsultState,
        on_delete=models.NOT_PROVIDED,
        default=1,
        verbose_name=_('Текущее состояние'),
    )

    cost = models.PositiveIntegerField(_('Цена консультации'))

    class Meta:
        verbose_name = _('Платная консультация')
        verbose_name_plural = _('Платные консультации')

    # Оплачена, если состояние не равно 'new'
    @property
    def is_paid(self):
        return self.state.key != 'new'

    # Переводим заявку в статус «Оплачено»
    def to_paid(self):
        if self.state.key == 'new':
            self.state = ConsultState.objects.get(key='paid')
            self.save()
            self.question.is_pay = True
            self.question.save()
            return True
        return False

    # Переводим заявку в статус «В работе», если есть user_id, то назначаем эксперта
    def to_in_work(self, user_id=None):
        if self.state.key != 'new':
            if user_id is not None:
                self.expert.add(user_id)
            self.state = ConsultState.objects.get(key='inwork')
            self.save()
            return True
        return False

    # Переводим заявку в статус «Ответ юриста»
    def to_answered(self):
        if self.state.key == 'answered':
            return True
        if self.state.key == 'inwork':
            self.state = ConsultState.objects.get(key='answered')
            self.save()
            return True
        return False

    # Переводим заявку в статус «Ответ юриста»
    def to_closed(self):
        if self.state.key == 'answered':
            self.state = ConsultState.objects.get(key='closed')
            self.save()
            return True
        return False

    def __str__(self):
        return self.question.__str__()


class ConsultStateLog(models.Model):
    """
    Журнал состояний консультации
    """
    consult = models.ForeignKey(Consult, on_delete=models.CASCADE)

    consult_state = models.ForeignKey(
        ConsultState,
        on_delete=models.CASCADE,
        verbose_name=_('Состояние')
    )

    date = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = _('Платные консультации: журнал состояний')
        verbose_name_plural = _('Платные консультации: журнал состояний')

    def __str__(self):
        return '%s (%s)' % (self.consult_state, self.date)


def post_save_answer_receiver(sender, instance, *args, **kwargs):
    """
    Добавление или удаление ответа
    """

    # Если удаляем ответ, то должны из общего количества должны отнять 1,
    # так как сигнал у нас, перед удалением.
    if 'created' in kwargs:
        i = 0
    else:
        i = 1

    question = instance.on_question

    # Подсчёт количества ответов на вопрос и «ответов» на ответ
    if instance.is_parent:
        question.reply_count = \
            sender.objects.filter(parent=None, on_question=question.pk).count() - i
        question.save(update_fields=('reply_count',))
    else:
        parent = instance.parent
        parent.reply_count = \
            sender.objects.filter(parent=parent.pk).count() - i
        parent.save(update_fields=('reply_count',))

post_save.connect(post_save_answer_receiver, sender=Answer)
pre_delete.connect(post_save_answer_receiver, sender=Answer)


def post_save_like_receiver(sender, instance, *args, **kwargs):
    """
    Добавление или удаление лайка. Считаем суммы баллов и кешируем в entry.like_count
    """
    cursor = connection.cursor()
    cursor.execute("""
      UPDATE entry_entry SET entry_entry.like_count = 
        (SELECT SUM(value) FROM entry_likes WHERE entry_id = %s)
      WHERE id = %s LIMIT 1
    """, [instance.entry.pk, instance.entry.pk])

post_save.connect(post_save_like_receiver, sender=Likes)
post_delete.connect(post_save_like_receiver, sender=Likes)


def add_to_consult_state_log_receiver(sender, instance, *args, **kwargs):
    """
    Добавляем запись в журнал состояний при изменении состояния консультации
    """
    c = ConsultStateLog.objects.create(consult=instance, consult_state=instance.state)
    c.save()

post_save.connect(add_to_consult_state_log_receiver, sender=Consult)