from django.db import models


class RubricManager(models.Manager):

    def get_queryset(self):
        """
        Только опубликованные рубрики
        """
        return super(RubricManager, self).get_queryset().filter(is_public=True)

