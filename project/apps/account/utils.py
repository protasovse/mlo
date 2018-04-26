from django.db import connection

from apps.account.models import Info


def delete_nonexistent_photos():
    """
    Удаляем из базы фото, файлов который нет
    :return:
    """
    info = Info.objects.all()
    for i in info:
        try:
            print(i.orig.file)
        except:
            i.orig = None
            i.pic = ''
            i.photo = ''
            i.save()


# Обновляем количество ответов у юристов
def recount_answer_count_on_account_info():
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE account_info SET
              answer_count = (
                SELECT COUNT(*) FROM entry_answer
                LEFT JOIN entry_entry ON (entry_entry.id = entry_answer.entry_ptr_id)
                WHERE 
                  entry_entry.author_id = account_info.user_id AND
                  parent_id IS NULL
              )
    """)


# Обновляем количество положительных отзывов у юристов
def recount_review_count_on_account_info():
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE account_info SET
          review_count = (
            SELECT COUNT(*) FROM review_likes
            LEFT JOIN entry_entry ON (entry_entry.id = review_likes.entry_id)
            WHERE entry_entry.author_id = account_info.user_id AND review_likes.value > 0
          )
    """)


# Обновляем стаж, вычисляем на основе введённого опыта работы
def recount_stage_on_account_info(user_id=None):
    where = 'WHERE account_info.user_id = {:d}'.format(user_id) if user_id else ''
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE account_info SET
          stage = IFNULL(
          (SELECT IF(
            (SELECT COUNT(*) FROM account_experience AS t1 WHERE t1.user_id=account_experience.user_id AND `finish` IS NULL),
             TIMESTAMPDIFF(SECOND, MIN(`start`), NOW()),
             TIMESTAMPDIFF(SECOND, MIN(`start`), MAX(`finish`))
          )/60/60/24/365 as period
          FROM account_experience WHERE account_experience.user_id = account_info.user_id)
          , 0) {}
    """.format(where))
