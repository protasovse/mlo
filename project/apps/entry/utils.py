from django.db import connection


# Обновляем количество ответов на записях
def recount_reply_count():
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE entry_entry SET
              reply_count = (
                SELECT COUNT(*) FROM entry_answer
                WHERE 
                  on_question_id = entry_entry.id AND
                  parent_id IS NULL
              )
        WHERE 
              entry_entry.id IN (SELECT on_question_id FROM entry_answer)
    """)


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
