from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView
from apps.entry.models import Question
from apps.rubric.models import Rubric


class QuestionsFeedList(ListView):
    context_object_name = 'questions'
    paginate_by = 30
    page_kwarg = 'page'

    def get_template_names(self):
        return 'entry/questions_feed_list.html'

    def get_queryset(self):
        return Question.published.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

