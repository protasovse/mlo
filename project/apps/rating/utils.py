from django.db import connection


# Пересчитываем рейтинг для всех юристов
def recount():
    cursor = connection.cursor()
    cursor.execute("""
      REPLACE rating_rating
      (user_id, rate, day_rate, week_rate, month_rate)
      SELECT
          id,
          IFNULL((
              SELECT SUM(t.value) FROM rating_ratingscore s
              LEFT JOIN rating_type t ON (s.type_id = t.id)
              WHERE s.user_id = u.id
          ), 0),
          IFNULL((
              SELECT SUM(t.value) FROM rating_ratingscore s
              LEFT JOIN rating_type t ON (s.type_id = t.id)
              WHERE s.user_id = u.id AND date >= DATE_SUB(NOW(), INTERVAL 1 DAY)), 0),
          IFNULL((
              SELECT SUM(t.value) FROM rating_ratingscore s
              LEFT JOIN rating_type t ON (s.type_id = t.id)
              WHERE s.user_id = u.id AND date >= DATE_SUB(NOW(), INTERVAL 7 DAY)), 0),
          IFNULL((
              SELECT SUM(t.value) FROM rating_ratingscore s
              LEFT JOIN rating_type t ON (s.type_id = t.id)
              WHERE s.user_id = u.id AND date >= DATE_SUB(NOW(), INTERVAL 1 MONTH)), 0)
	  FROM mlo_auth_user u WHERE role = 2;
    """)


# Добавить балл к рейтингу пользователя
def add_score(user_id, score):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE rating_rating SET
              rate = rate + {score},
              day_rate = day_rate + {score},
              week_rate = week_rate + {score},
              month_rate = month_rate + {score}
        WHERE 
              user_id = {user_id}
    """.format(user_id=user_id, score=score))
