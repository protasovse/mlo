from django.contrib.auth import get_user_model
from django.db import models

from apps.mlo_auth.managers import LAWYER
from config.settings import AUTH_USER_MODEL

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

    def related_to_question(self, question_id):
        """
        Выборка всех ответов, всех уровней, относящихся к вопросу question_id
        :param question_id: номер вопроса
        :return: queryset
        """
        qs = super(AnswersManager, self).filter(entry_id=question_id)
        return qs

    def by_question(self, question_id):
        """
        Ответы 1-го уровня на вопрос question_id
        :param question_id: номер вопроса
        :return: queryset
        """
        qs = self.related_to_question(question_id).filter(parent=None)
        return qs

    def create(self, question_id, content, author, parent=None):
        """
        Создаём ответ пользоваетеля на вопрос.
        :param question_id: вопрос, на который создаём ответ
        :param content: текс ответа
        :param author: автор ответа
        :param parent: если ответ не 1-го уровня, то задаёт родительский ответ
        :return: созданный ответ
        """

        if isinstance(author, get_user_model()):
            instance = self.model()
            instance.entry_id = question_id
            instance.author = author
            instance.content = content
            instance.parent = parent
            instance.save()
            return instance

        return None
