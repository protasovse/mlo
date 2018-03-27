from django.db import models


class AdviceManager(models.Manager):

    def get_queryset(self):
        return super(AdviceManager, self).get_queryset().select_related(
                'expert', 'expert__info', 'expert__city'
            ).all()
