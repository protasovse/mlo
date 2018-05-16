import pymorphy2
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import TemplateView, ListView

from apps.entry.models import Question
from apps.rating.models import Rating
from apps.review.models import Review, Likes
from apps.sxgeo.models import Cities


class Mainpage(TemplateView):
    template_name = 'front/index.html'

    def get_context_data(self, **kwargs):
        context = super(Mainpage, self).get_context_data(**kwargs)
        context['h1'] = "Консультация юриста онлайн"

        context['questions'] = Question.published.filter(reply_count__gt=0).order_by('-pk')[:5]
        context['lawyers'] = Rating.lawyers.filter(month_rate__gt=0)[:15]
        context['reviews'] = Review.objects.all()[:8]

        return context


class LawyerPage(TemplateView):
    template_name = 'front/lawyer_page.html'

    def get_context_data(self, **kwargs):
        context = super(LawyerPage, self).get_context_data(**kwargs)

        try:
            lawyer = get_user_model().objects.get(pk=kwargs['id'], role__gt=1, is_active=True)
        except ObjectDoesNotExist:
            raise Http404

        questions = Question.published.search('', 0, 10, {'answers_authors_id': (lawyer.pk,)})

        context.update({
            'likes': Likes.objects.filter(entry__author=lawyer, user__role=1).order_by("-date")[:10],
            'lawyer': lawyer,
            'questions': questions,
            'questions_count': questions.count,
        })

        return context


class LawyersListPage(ListView):
    template_name = 'front/lawyers_list_page.html'
    context_object_name = 'lawyers_list'
    paginate_by = 10
    paginate_orphans = 4

    def get_queryset(self):
        qs = get_user_model().objects.\
            filter(role=2, is_active=True).\
            order_by('-rating__month_rate', '-info__answer_count')

        if 'city_id' in self.kwargs:
            qs = qs.filter(city_id=self.kwargs['city_id'])

        return qs

    def get_context_data(self, **kwargs):
        context = super(LawyersListPage, self).get_context_data(**kwargs)

        title = 'Юристы и адвокаты. Юридическая помощь и консультации на Мойюрист.онлайн'

        if 'city_id' in self.kwargs:
            if self.kwargs['city_id'] == 520555:
                city_name = 'Нижнего Новгорода'
            else:
                city = Cities.objects.get(pk=self.kwargs['city_id'])
                morph = pymorphy2.MorphAnalyzer()
                c = morph.parse(city.name_ru)[0]
                city_name = c.inflect({'gent'}).word.title()

            title = 'Юристы и адвокаты {}. Юридическая помощь и консультации на Мойюрист.онлайн'.format(city_name)
            context.update({
                'city_id': self.kwargs['city_id'],
                'city': c.inflect({'gent'}).word,
            })

        context.update({
            'title': title,
        })

        return context


class ReviewsPage(ListView):
    template_name = 'front/reviews_page.html'
    context_object_name = 'likes'
    paginate_by = 15
    paginate_orphans = 5

    def get_queryset(self):
        qs = Likes.objects.filter(user__role=1).order_by("-date")

        if 'id' in self.kwargs:
            return qs.filter(entry__author_id=self.kwargs['id'])

        return qs

    def get_context_data(self, **kwargs):
        context = super(ReviewsPage, self).get_context_data(**kwargs)
        lawyer = False
        # Отзывы юриста
        if 'id' in self.kwargs:
            try:
                lawyer = get_user_model().objects.get(pk=self.kwargs['id'], role__gt=1)
            except ObjectDoesNotExist:
                raise Http404
        context.update({
            'lawyer': lawyer,
            'like_positive_count': self.get_queryset().filter(value__gt=0).count(),
            'like_negative_count': self.get_queryset().filter(value__lt=0).count(),
        })
        return context


class TermsOfUse(TemplateView):
    template_name = 'front/terms_of_use.html'


class About(TemplateView):
    template_name = 'front/about.html'
