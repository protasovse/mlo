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
    # return redirect(q, permanent=True)
    if 'page' in kwargs:
        return redirect('questions:list_tag', permanent=True, tag=q.slug, page=kwargs['page'])
    else:
        return redirect('questions:list_tag', permanent=True, tag=q.slug)


def rubric(request, **kwargs):

    slug2 = kwargs['rubric_slug2']
    if slug2 == 'Drugie-voprosy':
        slug2 = 'Prochie-voprosy'

    if slug2 == 'Pensii':
        slug2 = 'Pensii-i-socobespechenie'

    if slug2 == 'Migracionnye-voprosy':
        pass

    try:
        r = Rubric.objects.get(slug2=slug2)
    except:
        return redirect('questions:list')

    if 'page' in kwargs:
        return redirect('questions:list_rubric', permanent=True, rubric_slug=r.slug, page=kwargs['page'])
    else:
        return redirect('questions:list_rubric', permanent=True, rubric_slug=r.slug)


def questions(request, **kwargs):
    if 'page' in kwargs:
        return redirect('questions:list', permanent=True, page=kwargs['page'])
    else:
        return redirect('questions:list', permanent=True)


def user(request, **kwargs):
    return redirect('lawyer_page', id=kwargs['id'])