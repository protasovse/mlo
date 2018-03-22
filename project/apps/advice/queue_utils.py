from django.contrib.auth import get_user_model
from django.db import connection

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


def queue_shift():
    """
    Меняет очерёдность в очереди
    """
    '''
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
    '''
    cursor = connection.cursor()
    cursor.execute("""
        START TRANSACTION;
        SELECT @i := (SELECT COUNT(`order`) FROM `advice_queue`);
        UPDATE `advice_queue` SET `order` = @i + (@i := `order`) - @i
        WHERE `is_active` ORDER BY `order`;
        COMMIT;
        """)

    return True  # first


def queue_get_first():
    """
    Возвращает первого в очереди
    """
    return Queue.objects.filter(is_active=True).first().expert


def queue_add_user(user_id):
    """
    Добавляет пользоваетля в очередь
    """
    cursor = connection.cursor()
    cursor.execute("""
        INSERT IGNORE INTO `advice_queue` (`expert_id`, `order`, `is_active`)
        SELECT {user_id}, IFNULL(MAX(`order`)+1, 1), true FROM `advice_queue`;
        """.format(user_id=user_id))


def queue_del_user(user_id):
    """
    Удаляет пользователя из очереди
    """
    cursor = connection.cursor()
    cursor.execute("""
        START TRANSACTION;
        SELECT @i := (SELECT `order` FROM `advice_queue` WHERE `expert_id`={user_id});
        UPDATE `advice_queue` SET `order`=`order`-1 WHERE `order`>@i;
        DELETE FROM `advice_queue` WHERE `expert_id`={user_id} LIMIT 1;
        COMMIT;
        """.format(user_id=user_id))
