import os
import binascii

import misaka
from django.db import models
from django.utils.text import Truncator
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps import get_file_path
from apps.entry.managers import EntryPublishedManager, DELETED, DRAFT, PUBLISHED, BLOCKED, AnswersManager, \
    QuestionsPublishedManager
from apps.rubric.models import Classified
from apps.svem_system.exceptions import BackendPublicException
from config.settings import AUTH_USER_MODEL
from django_mysql.models import EnumField
from apps.sxgeo.models import Cities


CONSULT_COST = 800

DEFAULT_RUBRIC = 1

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
    content, author
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
    # technical fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #
    like_count = models.IntegerField(
        _('Лайки'), db_index=True,
        default=0)

    reply_count = models.IntegerField(
        _('Ответов'), db_index=True,
        default=0)

    views_count = models.PositiveIntegerField(_('Колличество просмотров'), default=0)

    objects = models.Manager()
    published = EntryPublishedManager()

    def save(self, *args, **kwargs):
        return super(Entry, self).save(*args, **kwargs)

    def __str__(self):
        return "%s " % (self.content[:64])

    def __int__(self):
        return self.pk

    @property
    def html_content(self):
        """
        Возвращает "content" форматированное в HTML.
        """
        return misaka.html(self.content.replace("\n", "\n\n"))

    def upload_document(self, file):
        """"""
        if not self.pk:
            raise BackendPublicException('model not load')
        return Files.objects.create(entry=self, file=file)

    class Meta:
        # ordering = ("-id",)
        # abstract = True
        pass


class Files(models.Model):
    """
    Модель файлов, прикрепленных к записи.
    """
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name='files',
    )

    file = models.FileField(
        upload_to=get_file_path,
        verbose_name=_('Файл'),
    )

    name = models.CharField(
        max_length=255,
        default=None,
        editable=False,
    )

    directory_string_var = 'entries'

    def get_basename(self):
        if self.name:
            return self.name
        elif self.file.name:
            return os.path.basename(self.file.name)

    def get_public_data(self, is_show=True):
        return {
            'entry_id': self.entry_id,
            'filename': self.get_basename(),
            'path': "/storage/{}".format(self.file) if is_show else False
        }

    class Meta:
        verbose_name = _('Файл')
        verbose_name_plural = _('Файлы')

    def save(self, **kwargs):
        if self.name is None:
            self.name = self.file.name
        return super(Files, self).save()

    def __str__(self):
        return str(self.get_basename())


class Titled(models.Model):
    """
    Эту модель будут наследовать все совокупности записей,
    у которых кроме текстового содержания есть заголовок
    """
    title = models.CharField(blank=False, max_length=160, verbose_name=_('Заголовок'))

    class Meta:
        abstract = True


class QuestionManager(models.Manager):
    @classmethod
    def create_paid_question(cls, user, params):
        question = Question.objects.create(
            title=params['title'],
            content=params['content'],
            author_id=user.id,
            status=BLOCKED,
            is_pay=1,
            first_name=params['name'] if params['name'] else user.first_name,
            phone=params['phone'],
            city_id=user.city_id if user.city_id else params['city_id'],
            rubric_id=params['rubric_id']
        )

        return question

    @classmethod
    def create_free_question(cls, user, is_authenticated, params):
        token = None
        if is_authenticated:
            status = PUBLISHED
        else:
            token = binascii.hexlify(os.urandom(20)).decode()
            status = BLOCKED
        return Question.objects.create(
            title=params['title'],
            content=params['content'],
            author_id=user.id,
            status=status,
            is_pay=0,
            token=token,
            first_name=params['name'] if params['name'] else user.first_name,
            phone=params['phone'],
            city_id=user.city_id if user.city_id else params['city_id'],
            rubric_id=params['rubric_id']
        )


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

    status = EnumField(
        _('Статус'), db_index=True,
        choices=[DELETED, PUBLISHED, BLOCKED, DRAFT], default=PUBLISHED)

    token = models.CharField("Key", max_length=40, db_index=True, unique=True, null=True, blank=True)

    first_name = models.CharField(_('first name'), max_length=32, blank=True)

    phone = models.CharField(max_length=15, blank=True, verbose_name=_('Телефон'))

    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, blank=True, null=True)

    objects = QuestionManager()
    published = QuestionsPublishedManager()

    class Meta:
        verbose_name = _("Вопрос")
        verbose_name_plural = _("Вопросы")

    def get_public_data(self):
        return {
            'id': self.id,
            'author': self.author.get_public_data()
        }

    def get_absolute_url(self):
        return reverse('question:detail', kwargs={'pk': self.pk})

    # Получаем список ответов на вопрос. Оптимизировано.
    def get_answers(self):
        return Answer.published.by_question(self.pk)

    def confirm(self):
        self.status = PUBLISHED
        self.save()
        # find user from hash
        user = self.author
        # if user doesnt active
        user.activate(False)
        # save to user personal info from question
        user.first_name = self.first_name
        user.city_id = self.city_id
        user.phone = self.phone
        user.save()

    def pay(self):
        self.confirm()

    def create(self):
        super()

    def __str__(self):
        return '№%d. %s: (%s)' % (self.pk, self.title, self.get_status_display())


class Answer(Entry):
    """
    Ответы на вопросы. Ответ относится к определенному вопросу.
    Так же ответ может относиться к вопросу и другому ответу на этот вопрос, т.е. юрист может добавить только
    один ответ, который относится только к вопросу. Далее диалог между клиентом и юристом будет происходить
    «под» 1-м ответом юриста на вопрос.

    on_question, parent_id,

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

    thread = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_('Ветка'),
    )

    status = EnumField(
        _('Статус'), db_index=True,
        choices=[DELETED, PUBLISHED, BLOCKED, DRAFT], default=PUBLISHED)

    objects = models.Manager()
    # Менеджер для публикации на публичной версии сайта
    published = AnswersManager()

    class Meta:
        ordering = ('thread', 'pk', )
        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')

    def children(self):
        return Answer.published.related_to_question(self.on_question_id).filter(parent=self)

    @property
    def is_parent(self):
        """
        Если True, то является первым ответом пользователя на вопрос
        """
        if self.parent_id is not None:
            return False
        return True

    @property
    def get_review(self):
        """
        Возвращает отзыв клиента, если такой есть.
        """
        return self.likes.filter(user=self.on_question.author).first()

    def get_public_data(self):
        return {
            'id': self.id,
            'pub_date_c': self.pub_date.isoformat() if self.pub_date else '',
            'pub_date': self.pub_date.strftime('%d %B %Y %H:%M') if self.pub_date else '',
            'parent_id': self.parent_id,
            'author': self.author.get_public_data(),
            'thread': self.thread,
            'content': self.html_content,
            'short_content': Truncator(self.content).words(10, truncate=' ...'),
            'like_count': self.like_count,
        }

    def get_like_data(self, request_user):
        """
        :param request_user :
        :return:
        """
        data = {
            'id': self.id,
            'is_can': False,
            'like_count': self.like_count
        }
        if not request_user.is_authenticated:
            return data

        return data

    def save(self, *args, **kwargs):

        if not hasattr(self, 'on_question'):
            self.on_question = self.parent.on_question

        super(Answer, self).save()

        if not hasattr(self, 'thread') or self.thread is None:
            self.thread = self.pk if self.is_parent else self.parent_id
            super(Answer, self).save(update_fields=['thread'])

        return self


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


class Additionals(models.Model):
    """
    Уточнения на вопрос. На какой вопрос, в ветки какого юриста
    """
    question_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        unique_together = ['question_id', 'user_id']


# Счётчик для SphinxSearch
class SphCounter(models.Model):
    counter_id = models.IntegerField(
        primary_key=True,
        auto_created=True,
    )

    max_id = models.IntegerField()


class Tag(models.Model):
    """
    Техническая модель для редиректа ссылок с тегом со Svem.ru
    на новые ссылки
    Экспорт — mlo_new процедура: call mlo_new.export_tags_from_svem();
    """
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    count = models.IntegerField()

    def get_absolute_url(self):
        return reverse('questions:list_tag', kwargs={'tag': self.slug})
