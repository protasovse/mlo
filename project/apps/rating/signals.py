from django.db.models.signals import post_save, post_delete

from apps.rating.models import RatingScore


def rating_calculation_receiver(sender, instance, *args, **kwargs):
    """
    Подсчёт рейтинга, после добавления или удаления балла
    """
    from .utils import recount
    recount(instance.user_id)


post_save.connect(rating_calculation_receiver, sender=RatingScore)
post_delete.connect(rating_calculation_receiver, sender=RatingScore)

'''
# Юрист отвечает на вопрос — добавляем балл рейтинга
def add_answer(sender, instance, *args, **kwargs):

    if 'created' in kwargs and kwargs['created']:
        # Если первый ответ
        if instance.is_parent:
            Rating.objects.create(
                type=RatingTypes.objects.get(key='answer'),
                user=instance.author,
                comment='За ответ %d' % (instance.pk,)
            )
        # если дополнительный ответ
        else:
            Rating.objects.create(
                type=RatingTypes.objects.get(key='add_answer'),
                user=instance.author,
                comment='За дополнительный ответ %d' % (instance.pk,)
            )


post_save.connect(expert_add_answer, sender=Answer, dispatch_uid='signal_expert_add_answer')
'''