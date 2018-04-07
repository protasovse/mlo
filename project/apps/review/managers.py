from django.db import models


class ReviewManager(models.Manager):

    def get_queryset(self):
        return super(ReviewManager, self).get_queryset().select_related(
                'like', 'like__user', 'like__entry__answer', 'like__entry__answer__on_question', 'like__user__city'
            ).prefetch_related()


class LikeManager(models.Manager):

    def get_queryset(self):
        return super(LikeManager, self).get_queryset().select_related(
                'user', 'entry__answer', 'review', 'entry__answer__on_question'
            ).prefetch_related()
