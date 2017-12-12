from django.views.generic import DetailView

from entry.models import Question


class QuestionDetail(DetailView):
    queryset = Question.published.all()
    context_object_name = 'question'
