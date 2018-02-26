from django.views.generic import DetailView, ListView

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


class QuestionsFeedList(ListView):
    context_object_name = 'questions'
    paginate_by = 3
    page_kwarg = 'page'

    def get_template_names(self):
        return 'entry/questions_feed_list.html'

    def get_queryset(self):
        return Question.published.all()

    def get_context_data(self, **kwargs):
        context = super(QuestionsFeedList, self).get_context_data(**kwargs)
        return context


class QuestionsList(ListView):
    template_name = 'entry/questions_list.html'
    context_object_name = 'questions'
    queryset = Question.published.all()
    paginate_by = 10
    page_kwarg = 'page'
