from collections import namedtuple

from django.contrib.auth import get_user_model
from django.db import connection
from django.views.generic import DetailView

from apps.account.models import RatingResult
from apps.entry.models import Question, Answer


class QuestionDetail(DetailView):
    queryset = Question.published.all()
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        """
        cursor = connection.cursor()
        cursor.execute("/""
          SELECT mau.* FROM account_ratingresult ar
          LEFT JOIN mlo_auth_user mau ON (mau.id = ar.user_id) 
          LEFT JOIN account_info ai ON (mau.id = ar.user_id) 
          ORDER BY `value` DESC LIMIT 10
          "/"")
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        context['rating'] = [nt_result(*row) for row in cursor.fetchall()]
        print(context['rating'])
        """
        context['rating'] = RatingResult.objects.all().order_by('-value')[:5]

        context['answers'] = Answer.answers.related_to_question(context['object']).filter(parent_id=None)

        return context
