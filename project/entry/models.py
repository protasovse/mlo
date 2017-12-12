import misaka

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from entry.managers import EntryPublishedManager, DELETED, DRAFT, PUBLISHED, AnswersManager
from entry.rubric.models import Classified
from mlo_rest.settings import AUTH_USER_MODEL

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
    Вопросы
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
    # К какой записи (вопросу) относится, так же равна question.pk
    entry_id = models.PositiveIntegerField(db_index=True)
    # Если является ответом на ответ, то содержит внешний ключ на этот ответ
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    answers = AnswersManager()

    class Meta:
        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')

    def children(self):
        return Answer.answers.related_to_question(self.entry_id).filter(parent=self)

    @property
    def is_parent(self):
        """
        Если True, то является первым ответом пользователя на вопрос
        """
        if self.parent is not None:
            return False
        return True

    @property
    def on_question(self):
        """
        Возвращаем вопрос на который ответ
        """
        return Question.objects.get(pk=self.entry_id)


def post_save_answer_receiver(sender, instance, *args, **kwargs):
    if instance.is_parent:
        question = instance.on_question
        question.reply_count = \
            sender.objects.filter(parent=None, entry_id=question.pk).count()
        question.save(update_fields=('reply_count',))
    else:
        parent = instance.parent
        parent.reply_count = \
            sender.objects.filter(parent=parent.pk).count()
        parent.save(update_fields=('reply_count',))

post_save.connect(post_save_answer_receiver, sender=Answer)
post_delete.connect(post_save_answer_receiver, sender=Answer)