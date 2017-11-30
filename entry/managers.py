from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.mlo_auth.managers import LAWYER
from mlo_rest.settings import AUTH_USER_MODEL

DELETED = 0
DRAFT = 1
PUBLISHED = 2


def entries_published(queryset):
    """
    Возвращает только опубликованные записи.
    """
    return queryset.filter(status=PUBLISHED)


class EntryPublishedManager(models.Manager):
    def get_queryset(self):
        return entries_published(super(EntryPublishedManager, self).get_queryset())


thread_data = None


class AnswersManager(models.Manager):

    def all(self):
        """
        Возвращаем только ответы 1-го уровня, у которых parent=None
        :return: queryset
        """
        qs = super(AnswersManager, self).filter(parent=None)
        return qs

    def answers_relate_to_question(self, question_id):
        """
        Выборка всех ответов, всех уровней, относящихся к вопросу question_id
        :param question_id: номер вопроса
        :return: queryset
        """
        qs = super(AnswersManager, self).filter(entry_id=question_id)
        return qs

    def answers_by_question(self, question_id):
        """
        Ответы 1-го уровня на вопрос question_id
        :param question_id: номер вопроса
        :return: queryset
        """
        qs = self.answers_relate_to_question(question_id).filter(parent=None)
        return qs

    def create(self, question_id, content, author):
        """
        Создаём основной ответ пользоваетеля на вопрос. Это может сделать юрист, и только один ответ
        :param question_id: вопрос, на который создаём ответ
        :param content: текс ответа
        :param author: автор ответа
        :return: созданный ответ
        """

        # if hasattr(author, 'role') is False or author.role != LAWYER:
        #     raise ValueError(_('Только юрист может отвечать на вопрос.'))
        #
        # if self.answers_by_question(question_id=question_id).filter(author=author).count() > 0:
        #     raise ValueError(_('Вы уже отвечали на этот вопрос.'))

        if isinstance(author, get_user_model()):
            instance = self.model()
            instance.entry_id = question_id
            instance.author = author
            instance.content = content
            instance.parent = None
            instance.save()
            return instance

        return None
