from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import RedirectView

from apps.entry.models import Question


class Redirect(RedirectView):
    pass


def question(request, **kwargs):
    q = get_object_or_404(Question, pk=kwargs['question_id'])
    return redirect(q, permanent=True)


def tag(request, **kwargs):
    q = get_object_or_404(Question, pk=kwargs['question_id'])
    return redirect(q, permanent=True)


def red(request):
    return HttpResponse('html')