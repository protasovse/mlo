import misaka
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.entry.managers import EntryPublishedManager, DELETED, DRAFT, PUBLISHED, AnswersManager
from apps.rubric.models import Classified
from config.settings import AUTH_USER_MODEL

STATUS_CHOICES = ((DELETED, _('Удалённый')),
                  (DRAFT, _('Черновик')),
                  (PUBLISHED, _('Опубликован')))


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
        _('Количество ответов'), db_index=True,
        default=0, editable=False)

    objects = models.Manager()
    published = EntryPublishedManager()

    def save(self, *args, **kwargs):
        return super(Entry, self).save(*args, **kwargs)

    def __str__(self):
        return '№%d. %s: (%s)' % (self.id, self.content[:40], self.get_status_display())

    def __int__(self):
        return self.pk

    @property
    def html_content(self):
        """
        Возвращает "content" форматированное в HTML.
        """
        return misaka.html(self.content)

    class Meta:
        abstract = True


class Files(models.Model):
    """
    Модель файлов, прикрепленных к записи.
    """
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='entries/files/%Y/%m/%d', verbose_name=_('Файл'))

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
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('entry', 'user')


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
    on_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    # Если является ответом на ответ, то содержит внешний ключ на этот ответ
    # parent — либо None, если ответ юриста первый, либо равен answer_id первого ответа.
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

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
        if self.parent is not None:
            return False
        return True


class Offer(models.Model):
    """
    Предложение платных услуг юристом
    """
    pass


def post_save_answer_receiver(sender, instance, *args, **kwargs):
    """
    Сигнал для подсчёта количества ответов на вопрос
    и «ответов» на ответ
    """
    if instance.is_parent:
        question = instance.on_question
        question.reply_count = \
            sender.objects.filter(parent=None, on_question=question.pk).count()
        question.save(update_fields=('reply_count',))
    else:
        parent = instance.parent
        parent.reply_count = \
            sender.objects.filter(parent=parent.pk).count()
        parent.save(update_fields=('reply_count',))

post_save.connect(post_save_answer_receiver, sender=Answer)
post_delete.connect(post_save_answer_receiver, sender=Answer)
