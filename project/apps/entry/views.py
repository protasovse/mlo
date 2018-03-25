from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView
from apps.entry.models import Question
from apps.rubric.models import Rubric


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


class QuestionsList(TemplateView):
    template_name = 'entry/questions_list.html'
    # context_object_name = 'questions'
    # queryset = Question.published.all()
    # paginate_by = 10
    # page_kwarg = 'page'

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
        # context['rating'] = RatingResult.objects.all().order_by('-value')[:5]

        # Вопросы
        context['questions'] = Question.published.by_rubric(68)[:10]

        return context
