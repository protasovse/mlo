from django.db import connection


def recount(user_id):

    cursor = connection.cursor()

    cursor.execute("""
      REPLACE rating_rating
        (user_id, rate, day_rate, week_rate, month_rate)
        VALUES (
          {user_id},
    
          IFNULL((
              SELECT SUM(t.value) FROM rating_ratingscore s
              LEFT JOIN rating_type t ON (s.type_id = t.id)
              WHERE user_id = {user_id}
          ), 0),
    
          IFNULL((
              SELECT SUM(t.value) FROM rating_ratingscore s
              LEFT JOIN rating_type t ON (s.type_id = t.id)
              WHERE user_id = {user_id} AND date >= DATE_SUB(NOW(), INTERVAL 1 DAY)), 0),
    
          IFNULL((
              SELECT SUM(t.value) FROM rating_ratingscore s
              LEFT JOIN rating_type t ON (s.type_id = t.id)
              WHERE user_id = {user_id} AND date >= DATE_SUB(NOW(), INTERVAL 7 DAY)), 0),
    
          IFNULL((
              SELECT SUM(t.value) FROM rating_ratingscore s
              LEFT JOIN rating_type t ON (s.type_id = t.id)
              WHERE user_id = {user_id} AND date >= DATE_SUB(NOW(), INTERVAL 1 MONTH)), 0)
        );
    """.format(user_id=user_id))


def add_score(score, user_id):

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