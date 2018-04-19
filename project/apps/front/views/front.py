from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.entry.models import Question
from apps.rating.models import Rating
from apps.review.models import Review, Likes


class Mainpage(TemplateView):
    template_name = 'front/index.html'

    def get_context_data(self, **kwargs):
        context = super(Mainpage, self).get_context_data(**kwargs)
        context['h1'] = "Консультация юриста онлайн"

        context['questions'] = Question.published.filter(reply_count__gt=0, is_pay=True).order_by('-pk')[:5]
        context['lawyers'] = Rating.lawyers.filter(month_rate__gt=0)[:15]
        context['reviews'] = Review.objects.all()[:8]

        return context


class LawyerPage(TemplateView):
    template_name = 'front/lawyer_page.html'

    def get_context_data(self, **kwargs):
        context = super(LawyerPage, self).get_context_data(**kwargs)

        try:
            lawyer = get_user_model().objects.get(pk=kwargs['id'], role__gt=1)
        except ObjectDoesNotExist:
            raise Http404

        context.update({
            'likes': Likes.objects.filter(entry__author=lawyer, user__role=1).order_by("-date")[:10],
            'lawyer': lawyer,
            'questions': Question.published.search('', 0, 10, {'answers_authors_id': (lawyer.pk,)})
        })

        return context


class ReviewsPage(TemplateView):
    template_name = 'front/reviews_page.html'

    def get_context_data(self, **kwargs):

        context = super(ReviewsPage, self).get_context_data(**kwargs)
        likes = Likes.objects.filter(user__role=1).order_by("-date")
        lawyer = None

        # Отзывы юриста
        if 'id' in kwargs:
            likes = likes.filter(entry__author_id=kwargs['id'])
            try:
                lawyer = get_user_model().objects.get(pk=kwargs['id'], role__gt=1)
            except ObjectDoesNotExist:
                raise Http404

        context.update({
            'likes': likes[:40],
            'lawyer': lawyer,
            'like_positive_count': likes.filter(value__gt=0).count(),
            'like_negative_count': likes.filter(value__lt=0).count(),
        })

        return context


class TermsOfUse(TemplateView):
    template_name = 'front/terms_of_use.html'


class About(TemplateView):
    template_name = 'front/about.html'
