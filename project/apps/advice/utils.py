from django.db import connection

from apps.advice.models import Queue, Scheduler


def queue_update():
    """
    Здесь нужно проверить условия, может ли пользователь быть в очереди и обновить его активность.
    """
    cursor = connection.cursor()
    cursor.execute("""
        START TRANSACTION;
        UPDATE `advice_queue` SET `is_active` = false;
        UPDATE `advice_queue` SET `is_active` = true
        WHERE `expert_id` IN (
            SELECT `expert_id` FROM `advice_scheduler` 
            WHERE
                `is_available` AND
                (CURTIME() >= `begin` AND CURTIME() <= `end`) AND
                (`weekend` OR WEEKDAY(NOW()) NOT IN (5, 6))
        );
        COMMIT;
    """)


def queue_shift():
    """
    Меняет очерёдность в очереди
    """
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
    Возвращает первого в очереди пользователя и смещает очередь
    """
    queue_update()
    first = Queue.objects.filter(is_active=True).first()
    if first:
        queue_shift()
        return first.expert


def queue_add_user(user_id):
    """
    Добавляет пользователя в очередь
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
