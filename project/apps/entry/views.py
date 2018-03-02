from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from apps.account.models import RatingResult
from apps.entry.models import Question, Answer
from apps.rubric.models import Rubric


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
        context = super().get_context_data(**kwargs)
        return context


class QuestionsList(ListView):
    template_name = 'entry/questions_list.html'
    context_object_name = 'questions'
    queryset = Question.published.filter(reply_count__gt=0)
    paginate_by = 10
    page_kwarg = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Выборка информации о рубриках
        if 'subrubric_slug' in self.kwargs:
            slug = self.kwargs['subrubric_slug']
        elif 'rubric_slug' in self.kwargs:
            slug = self.kwargs['rubric_slug']
        else:
            slug = ''
        # Получаем всех предков
        if slug:
            rubric = get_object_or_404(Rubric, slug=slug)
            rubrics = rubric.get_ancestors(include_self=True)
            if rubrics[0].slug != self.kwargs['rubric_slug']:
                raise Http404()
            context['rubrics'] = rubrics

        # Все рубрики
        context['all_rubrics'] = Rubric.objects.filter(level=0)

        # Лучшие юристы
        context['rating'] = RatingResult.objects.all().order_by('-value')[:5]

        return context
