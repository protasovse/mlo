from django.db import models


class ReviewManager(models.Manager):

    def get_queryset(self):
        return super(ReviewManager, self).get_queryset().select_related(
                'like', 'like__user'  # , 'like__entry__answer__on_question', 'like__user__city'
            ).prefetch_related()


class LikeManager(models.Manager):

    def get_queryset(self):
        return super(LikeManager, self).get_queryset().select_related(
                'review', 'entry__answer__on_question', 'user__city', 'entry__author'
            ).prefetch_related()
