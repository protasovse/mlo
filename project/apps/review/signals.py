from django.db import connection
from django.db.models.signals import post_save, post_delete

from apps.review.models import Likes


def add_like_receiver(sender, instance, *args, **kwargs):
    """
    Добавление или удаление лайка. Считаем суммы баллов и кешируем в entry.like_count
    """
    cursor = connection.cursor()
    cursor.execute("""
      UPDATE entry_entry SET entry_entry.like_count = 
        (SELECT SUM(value) FROM review_likes WHERE entry_id = '%s')
      WHERE id = '%s' LIMIT 1
    """, [instance.entry.pk, instance.entry.pk])

# post_save.connect(add_like_receiver, sender=Likes)
# post_delete.connect(add_like_receiver, sender=Likes)