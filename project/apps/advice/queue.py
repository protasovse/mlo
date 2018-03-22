from django.contrib.auth import get_user_model

from apps.advice.models import Queue


def update_expert_in_queue(user_id):
    """
    Здесь нужно проверить условия, может ли пользователь быть в очереди и обновить его активность.

    1. Пользователь есть в модели Expert, то

        1. Если пользователя нет в модели Scheduler, то
                Добавить со значениями по умолчанию

        2. Если пользователя нет в модели Queue, то
                Добавить с order = max(order)+1 и is_active=True
                можно return is_active

        3. Если текущая дата попадает в промежуток из модели Scheduler, то
                Queue.is_active=True
            иначе
                Queue.is_active=False

        return is_active

    иначе

        1. Если пользователь есть в модели Queue, то
            Queue.is_active=False

        return False
    """
    user = get_user_model().object.get(pk=user_id)


def shift_queue():
    """
    Меняет очерёдность в очереди
    """
    queue = Queue.objects.filter(is_active=True)
    # first = queue.first()
    last_order = queue.last().order

    order = 0
    for q in queue:
        swap_order = q.order
        if order == 0:
            q.order = last_order
            order = swap_order
        else:
            if q.is_active:
                q.order = order
                order = swap_order

        q.save(update_fields=['order', ])

    return True  # first


