from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.entry.models import Question
from apps.rating.models import Rating
from apps.review.models import Review


class Mainpage(TemplateView):
    template_name = 'front/index.html'

    def get_context_data(self, **kwargs):
        context = super(Mainpage, self).get_context_data(**kwargs)
        context['h1'] = "Консультация юриста онлайн"

        context['questions'] = Question.published.filter(reply_count__gt=0, is_pay=True).order_by('-pk')[:5]
        context['lawyers'] = Rating.lawyers.filter(month_rate__gt=0)[:15]
        context['reviews'] = Review.objects.filter(like__entry__answer__on_question__is_pay=True)[:5]

        return context


class LawyerPage(TemplateView):
    template_name = 'front/lawyer_page.html'

    def get_context_data(self, **kwargs):
        context = super(LawyerPage, self).get_context_data(**kwargs)

        try:
            lawyer = get_user_model().objects.get(pk=kwargs['id'], role__gt=1)
        except ObjectDoesNotExist:
            raise Http404

        context['lawyer'] = lawyer

        context.update({
            'reviews': Review.objects.filter(like__entry__author=lawyer)[:10]
        })

        return context


