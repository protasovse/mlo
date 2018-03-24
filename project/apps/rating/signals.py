from django.db.models.signals import post_save, post_delete

from apps.entry.models import Answer
from apps.rating.models import RatingScore, Type


def rating_calculation_receiver(sender, instance, *args, **kwargs):
    """
    Подсчёт рейтинга, после добавления или удаления балла
    """
    from .utils import add_score
    if 'created' in kwargs and kwargs['created']:
        add_score(instance.user_id, instance.type.value)
    elif 'created' not in kwargs:
        add_score(instance.user_id, -instance.type.value)
post_save.connect(rating_calculation_receiver, sender=RatingScore)
post_delete.connect(rating_calculation_receiver, sender=RatingScore)


# Юрист отвечает на вопрос — добавляем балл рейтинга
def add_answer(sender, instance, *args, **kwargs):

    if 'created' in kwargs and kwargs['created']:
        # Только для юриста
        if instance.author.role == 2:
            # Если первый ответ
            if instance.is_parent:
                RatingScore.objects.create(
                    type=Type.objects.get(key='answer'),
                    user=instance.author,
                    comment='За ответ %d' % (instance.pk,)
                )
            # если дополнительный ответ
            else:
                RatingScore.objects.create(
                    type=Type.objects.get(key='add_answer'),
                    user=instance.author,
                    comment='За уточнение %d' % (instance.pk,)
                )
post_save.connect(add_answer, sender=Answer, dispatch_uid='signal_expert_add_answer')
