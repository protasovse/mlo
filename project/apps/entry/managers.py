import sphinxapi
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
                'author', 'author__info', 'author__rating', 'author__city'
            ).prefetch_related()
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
    # Выборка всех ответов, всех уровней, относящихся к вопросу question_id
    def related_to_question(self, question_id):
        qs = super(AnswersManager, self).filter(on_question_id=question_id)
        return qs

    # Ответы 1-го уровня на вопрос question_id
    def by_question(self, question_id):
        qs = self.related_to_question(question_id).filter(parent=None)
        return qs


# Менеджер для вывода вопросов для публикации
class QuestionsPublishedManager(EntryPublishedManager):
    def get_queryset(self):
        return super(QuestionsPublishedManager, self).get_queryset().select_related(
            'rubric', 'advice'
        )

    def by_id(self, id_list):
        qs = super(QuestionsPublishedManager, self).filter(entry_ptr_id__in=id_list)
        return qs

    def by_keywords(self, keyword):
        qs = super(QuestionsPublishedManager, self).filter(content__icontains=keyword)
        return qs

    def by_rubric(self, rubric_id):
        qs = super(QuestionsPublishedManager, self).filter(rubrics__exact=rubric_id)
        return qs

    def search(self, query='', offset=0, limit=10, filters={}, sort=[]):
        """
        :param query:
        :param offset:
        :param limit:
        :param filters: Словарь фильтров
        :return:
        """

        client = sphinxapi.SphinxClient()
        client.SetServer('127.0.0.1', 9312)

        client.SetLimits(offset, limit, 1000)

        if not sort:
            sort.append('pub_date DESC')

        client.SetSortMode(sphinxapi.SPH_SORT_EXTENDED, ', '.join(sort))
        client.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED)

        for key in filters:
            client.SetFilter(key, filters[key])

        result = client.Query(query, 'question, question_delta')
        print(result)

        # ids = [r['id'] for r in result['matches']]
        if not result:
            return None

        qss = [self.get_queryset().filter(entry_ptr_id=r['id']) for r in result['matches']]
        qs = self.get_queryset().none().union(*qss)

        # qs = self.get_queryset().filter(entry_ptr_id__in=list(ids))

        qs.count = result['total_found']
        return qs
