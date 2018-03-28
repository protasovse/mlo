from django.db import models


class RatingLawyerManager(models.Manager):

    def get_queryset(self):
        return super(RatingLawyerManager, self).get_queryset().select_related(
                'user', 'user__info', 'user__city',
            ).prefetch_related()
