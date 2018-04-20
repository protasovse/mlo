from django.db import connection


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
