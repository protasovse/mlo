from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import RedirectView

from apps.entry.models import Question, Tag
from apps.rubric.models import Rubric


class Redirect(RedirectView):
    pass


def question(request, **kwargs):
    q = get_object_or_404(Question, pk=kwargs['question_id'])
    return redirect(q, permanent=True)


def tag(request, **kwargs):
    q = get_object_or_404(Tag, pk=kwargs['tag_id'])
    return redirect(q, permanent=True)


def rubric(request, **kwargs):
    r = get_object_or_404(Rubric, slug2=kwargs['rubric_slug2'])
    return redirect(r, permanent=True)