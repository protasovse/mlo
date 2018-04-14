from config import flash_messages
from django.http import Http404
from django.utils import timezone
from django.db import transaction
from django.utils.http import urlencode
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth import login
from apps.advice.models import Advice, ADVICE_PAYMENT_CONFIRMED
from apps.rating.models import Rating
from apps.rubric.models import Rubric
from apps.entry.models import Question, Answer
from django.contrib import messages
from django.urls import reverse
from datetime import timedelta
from apps.svem_system.exceptions import ControlledException
from django.shortcuts import get_object_or_404

from config.flash_messages import QUESTION_CREATE_PAID, QUESTION_CREATE_BLOCKED
from config.settings import ADVICE_OVERDUE_TIME, MONEY_YANDEX_PURSE, PAYMENT_FORM_TITLE, PAYMENT_FORM_TARGET, \
    ADVICE_COST


class QuestionDetail(TemplateView):
    template_name = 'question/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = get_object_or_404(Question, pk=kwargs['pk'])

        if question.status == 'blocked':
            ids = self.request.session.get('question_ids', [])
            if question.id not in ids and question.author != self.request.user:
                raise Http404("Question does not exist")

            messages.add_message(self.request, messages.WARNING,
                                 QUESTION_CREATE_PAID if question.is_pay else QUESTION_CREATE_BLOCKED)

        context.update({
            'question': question
        })

        if question.is_pay:
            advice = Advice.objects.filter(question=question).first()
            advice_context = {
                'advice': advice,
                'money_yandex_purse': MONEY_YANDEX_PURSE,
                'payment_form_title': PAYMENT_FORM_TITLE,
                'payment_form_target': PAYMENT_FORM_TARGET,
                'advice_cost': ADVICE_COST
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
    page_size = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Выборка информации о рубриках
        rubric = None
        rubrics_also_list = None
        rubrics_useful = None
        if 'rubric_slug' in self.kwargs:
            slug = self.kwargs['rubric_slug']
        else:
            slug = None
        # Получаем всех предков
        if slug:
            rubric = get_object_or_404(Rubric, slug=slug)
            rubrics = rubric.get_ancestors(include_self=True)
            rubrics_also_list = rubric.get_children().filter(is_question_rubric=True)
            rubrics_useful = rubric.get_children().filter(is_guide_rubric=True, is_question_rubric=False)
            # if rubrics[0].slug != self.kwargs['rubric_slug']:
            #     raise Http404()
            context['rubrics'] = rubrics
            context['rubric'] = rubric

        # Вычисляем страницу
        if 'page' in self.kwargs:
            current_page = self.kwargs['page']
            start = self.page_size * (current_page - 1)
        else:
            current_page = 1
            start = 0

        filters = {}
        sort = []
        query = ''
        current_url = reverse('questions:list')  # текущий url без параметров и страниц
        url_params = {}  # GET параметры для url, используется в пагинаторе

        # Вопросы
        if rubric:
            if rubric.keywords:
                query = '({})'.format(')|('.join(rubric.keywords.split("\n")))
                sort.append('@relevance DESC')

            else:
                filters.update({'rubric_id': (rubric.pk,)})

            current_url = reverse('questions:list_rubric', kwargs={
                'rubric_slug': rubric.slug
            })

        if 'paid' in self.request.GET:
            filters.update({'is_pay': (True,)})
            url_params.update({
                'paid': True
            })

        if 'free' in self.request.GET:
            filters.update({'is_pay': (False,)})
            url_params.update({
                'free': True
            })

        if 'my_advice' in self.request.GET:
            filters.update({'advice_expert_id': (self.request.user.pk,)})
            url_params.update({
                'my_advice': True
            })

        if 'unanswered' in self.request.GET:
            filters.update({'reply_count': (0,)})
            url_params.update({
                'unanswered': True
            })

        if 'additionals' in self.request.GET:
            filters.update({'additionals_user_id': (self.request.user.pk,)})
            url_params.update({
                'additionals': True
            })

        # filters.update({'answers_authors_id': (1,)})

        # QuerySet для списка вопросов
        question_set = Question.published.search(query, start, self.page_size, filters, sort)

        context.update({
            'current_url': current_url,
            'url_params': "?" + urlencode(url_params) if url_params else '',
            'total_found': question_set.count,
            'current_page': current_page,
            'next_page': current_page + 1 if current_page * self.page_size < question_set.count else None,
            'questions': question_set,
        })

        # Списки рубрик для aside «Темы консультаций, рубрикатор» и «Консультируем так же»
        context.update({
            'rubrics_list': Rubric.objects.filter(level__in=(0,), is_question_rubric=True),
            'rubrics_also_list': rubrics_also_list,
            'rubrics_useful': rubrics_useful,
            # 'rubrics_list': Rubric.rubricator.filter(level__in=(0,)),
        })

        # Лучшие юристы блок
        context.update({
            'lawyers_from_rating': Rating.lawyers.all()[:4]
        })

        return context


class AskQuestion(TemplateView):
    template_name = 'question/ask.html'


class ConfirmQuestion(RedirectView):
    def get_redirect_url(self, **kwargs):
        try:
            q = None
            with transaction.atomic():
                pk = kwargs['pk']
                token = kwargs['token']
                try:
                    q = Question.objects.get(token=token)
                except Question.DoesNotExist as e:
                    raise ControlledException(e)
                # do activate question
                if q.id != pk:
                    raise ControlledException()
                # to public the question
                q.confirm()
            # to do login user
            if not self.request.user.is_authenticated:
                login(self.request, q.author)
            return reverse('question:detail', kwargs={'pk': q.id})
        except ControlledException:
            messages.add_message(self.request, messages.ERROR, flash_messages.QUESTION_CONFIRM_ERROR, 'danger')
            return reverse('question:detail', kwargs={'pk': kwargs['pk']})
