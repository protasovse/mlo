from django.contrib.auth import get_user_model
from django.db import models


DELETED = 'deleted'
BLOCKED = 'blocked'
DRAFT = 'draft'
PUBLISHED = 'public'


def entries_published(queryset):
    """
    Возвращает только опубликованные записи.
    """
    return queryset.filter(status=PUBLISHED)


class EntryPublishedManager(models.Manager):
    def get_queryset(self):
        """
        Только опубликованные записи
        """
        return entries_published(
            super(EntryPublishedManager, self).get_queryset().select_related(
                'author', 'author__info', 'author__ratingresult', 'author__city'
            ).prefetch_related(
            )
        )

    def like(self, entry_id, user_id):
        """
        Установить/удалить лайк для записи с pk=entry_id, пользователем user_id
        :return: True если установили лайк, False если удалили
        """
        obj = self.model.objects.filter(pk=entry_id)
        if obj.count():
            obj = obj[0]
        else:
            return None
        like, created = obj.likes.get_or_create(entry_id=entry_id, user_id=user_id)
        if created:
            i_like_it = True
        else:
            like.delete()
            i_like_it = False

        return i_like_it


thread_data = None


class AnswersManager(EntryPublishedManager):

    def related_to_question(self, question_id):
        """
        Выборка всех ответов, всех уровней, относящихся к вопросу question_id
        :param question_id: номер вопроса
        :return: queryset
        """
        qs = super(AnswersManager, self).filter(on_question_id=question_id)
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
        :param content: текст ответа
        :param author: автор ответа
        :param parent: если ответ не 1-го уровня, то задаёт родительский ответ
        :return: созданный ответ
        """

        if isinstance(author, get_user_model()):
            instance = self.model()
            instance.on_question_id = question_id
            instance.author = author
            instance.content = content
            instance.parent = parent
            instance.save()
            return instance

        return None
