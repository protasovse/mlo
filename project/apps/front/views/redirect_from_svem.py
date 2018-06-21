from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import RedirectView

from apps.entry.models import Question, Tag
from apps.rubric.models import Rubric


def question(request, **kwargs):
    q = get_object_or_404(Question, pk=kwargs['question_id'])
    return redirect(q, permanent=True)


def tag(request, **kwargs):
    q = get_object_or_404(Tag, pk=kwargs['tag_id'])

    try:
        r = Rubric.objects.get(slug=q.slug)
    except Rubric.DoesNotExist:
        if 'page' in kwargs:
            return redirect('questions:list_tag', permanent=True, tag=q.slug, page=kwargs['page'])
        else:
            return redirect('questions:list_tag', permanent=True, tag=q.slug)
    return redirect('questions:list_rubric', permanent=True, rubric_slug=r.slug)


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
    return redirect('front:lawyer_page', permanent=True, id=kwargs['id'])


def review(request, **kwargs):
    if 'page' in kwargs:
        return redirect('front:reviews_page', permanent=True, page=kwargs['page'])
    else:
        return redirect('front:reviews_page', permanent=True)


def blog(request, **kwargs):

    if kwargs['slug'] == 'likbez':
        slug = 'юридический-ликбез'
    elif kwargs['slug'] == 'publication':
        slug = 'публикации'
    else:
        raise Http404("Article dir doesn't exists")

    return redirect(
        'article:article',
        permanent=True,
        slug=slug,
        id=str(int(kwargs['id'])+600000),
    )
