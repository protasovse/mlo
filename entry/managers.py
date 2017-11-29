from django.db import models

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
        qs = super(AnswersManager, self).filter(parent=None)
        return qs

    def answers_relate_to_question(self, question_id):
        qs = super(AnswersManager, self).filter(entry_id=question_id)
        return qs

    def answers_by_question(self, question_id):
        qs = self.answers_relate_to_question(question_id).filter(parent=None)
        return qs
