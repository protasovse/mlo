from django.http import Http404
from django.utils import timezone
from django.db import transaction
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth import login
from apps.advice.models import Advice, ADVICE_PAYMENT_CONFIRMED
from apps.rating.models import Rating
from apps.rubric.models import Rubric
from apps.svem_auth.models.users import UserHash
from apps.entry.models import Question, Answer
from apps.entry.managers import PUBLISHED
from django.contrib import messages
from django.urls import reverse
from datetime import date, timedelta
from apps.svem_system.exceptions import ControlledException
from django.shortcuts import get_object_or_404

from config.settings import ADVICE_OVERDUE_TIME


class QuestionDetail(TemplateView):
    template_name = 'question/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = get_object_or_404(Question, pk=kwargs['pk'])

        if question.status == 'blocked':
            ids = self.request.session.get('question_ids', [])
            if question.id not in ids:
                raise Http404("Question does not exist")

        context.update({
            'question': question
        })

        if question.is_pay:
            advice = Advice.objects.filter(question=question).first()
            advice_context = {
                'advice': advice
            }

            if advice and advice.status == ADVICE_PAYMENT_CONFIRMED:
                overdue_time = timedelta(minutes=ADVICE_OVERDUE_TIME) - (timezone.now() - advice.payment_date)
                advice_context.update({
                    'overdue_time': overdue_time.seconds // 60
                })

            context.update({
                'advice_context': advice_context
            })

        context.update({
            'mess': messages.get_messages(self.request),
            'answers': Answer.published.related_to_question(question)
        })

        # Лучшие юристы блок
        context.update({
            'lawyers_from_rating': Rating.lawyers.all()[:3]
        })

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
            # rubrics = rubric.get_ancestors(include_self=True)
            # if rubrics[0].slug != self.kwargs['rubric_slug']:
            #     raise Http404()
            # context['rubrics'] = rubrics
            context['rubric'] = rubric

        # Все рубрики
        context['all_rubrics'] = Rubric.objects.filter(level=0)

        # Вопросы
        if slug:
            # context['questions'] = Question.published.filter(rubric=rubric).order_by('-pk')[:10]
            context['questions'] = Question.published.search(rubric.name, 0, 10)
        else:
            context['questions'] = Question.published.order_by('-pk')[:10]

        # Список рубрик для aside
        context['rubrics_list'] = Rubric.objects.filter(level__in=(0, ))

        # Лучшие юристы блок
        context.update({
            'lawyers_from_rating': Rating.lawyers.all()[:3]
        })

        return context


class AskQuestion(TemplateView):
    template_name = 'question/ask.html'


class ConfirmQuestion(RedirectView):
    def get_redirect_url(self, **kwargs):

        try:
            with transaction.atomic():
                pk = kwargs['pk']
                token = kwargs['token']
                try:
                    hash_obj = UserHash.objects.get(key=token)
                except UserHash.DoesNotExist as e:
                    raise ControlledException(e)
                # if hash exists, but too late
                if hash_obj.live_until.date() < date.today():
                    raise ControlledException()
                # do activate question
                q = Question.objects.get(key=token)
                if q.id != pk:
                    raise ControlledException()
                # to public the question
                q.status = PUBLISHED
                q.save()
                # find user from hash
                user = hash_obj.user
                # if user doesnt active
                user.activate(False)
                # save to user personal info from question
                user.first_name = q.first_name
                user.city_id = q.city_id
                user.phone = q.phone
                user.save()
                # remove hash
                hash_obj.delete()
                # to do login user
                if not self.request.user.is_authenticated:
                    login(self.request, user)
            return reverse('question:detail', kwargs={'pk': q.id})
        except ControlledException:
            messages.add_message(
                self.request,
                messages.ERROR,
                '<h4>Произошла ошибка</h4> <p>Не удалось подтвердить вопрос</p>',
                'danger'
            )
            return reverse('question:detail', kwargs={'pk': kwargs['pk']})
