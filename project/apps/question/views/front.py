import urllib.parse

import re
from django.contrib.sites.models import Site
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from config import flash_messages
from django.http import Http404
from django.utils import timezone
from django.db import transaction
from django.utils.http import urlencode
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth import login, get_user_model
from apps.advice.models import Advice, ADVICE_PAYMENT_CONFIRMED
from apps.rating.models import Rating
from apps.rubric.models import Rubric
from apps.entry.models import Question, Answer, Tag
from django.contrib import messages
from django.urls import reverse
from datetime import timedelta
from apps.svem_system.exceptions import ControlledException
from django.shortcuts import get_object_or_404

from config.flash_messages import QUESTION_CREATE_PAID, QUESTION_CREATE_BLOCKED
from config.settings import ADVICE_OVERDUE_TIME, MONEY_YANDEX_PURSE, PAYMENT_FORM_TITLE, PAYMENT_FORM_TARGET, \
    ADVICE_COST, SITE_PROTOCOL


class QuestionDetail(TemplateView):
    template_name = 'question/question_detail.html'

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        question = get_object_or_404(Question, pk=pk)

        if question.status == 'blocked':
            ids = self.request.session.get('question_ids', [])

            if question.id not in ids and question.author != self.request.user:
                raise Http404("Question does not exist")

            messages.add_message(self.request, messages.WARNING,
                                 QUESTION_CREATE_PAID if question.is_pay else QUESTION_CREATE_BLOCKED)

        context.update({
            'question': question
        })

        question.views_count = F('views_count') + 1
        question.save(update_fields=['views_count'])

        # Выборка похожих вопросов
        query_for_similar_questions = '|'.join(re.split(r'[\s]+', question.title))
        # Выбираем, исключая сам вопрос
        similar_questions = Question.published.search(
            query=query_for_similar_questions,
            offset=0,
            limit=5,
            sort=['@relevance DESC', ],
            exclude_id=question.pk,
        )

        if hasattr(question, 'advice'):
            advice = Advice.objects.filter(question=question).first()
            advice_context = {
                'advice': advice,
                'money_yandex_purse': MONEY_YANDEX_PURSE,
                'payment_form_title': PAYMENT_FORM_TITLE,
                'payment_form_target': PAYMENT_FORM_TARGET,
                'advice_cost': ADVICE_COST,
            }

            if advice.status == ADVICE_PAYMENT_CONFIRMED:
                overdue_time = timedelta(minutes=ADVICE_OVERDUE_TIME) - (timezone.now() - advice.payment_date)
                advice_context.update({
                    'overdue_time': overdue_time.seconds // 60
                })

            context.update({
                'advice_context': advice_context
            })

        context.update({
            'mess': messages.get_messages(self.request),
            'answers': Answer.published.related_to_question(question),
            'question_url': urllib.parse.unquote(reverse('question:detail', kwargs={'pk': question.pk})),
            'similar_questions': similar_questions,
        })

        #if self.request.user.is_authenticated and self.request.user.role == 2:
           # context.update({
           #     'is_my_answer': not not Answer.objects.filter(on_question=question, author_id=self.request.user,
           #                                                   parent=None).count()
           # })

        # Лучшие юристы блок
        context.update({
            'lawyers_from_rating': Rating.lawyers.all()[:3],
            'lawyer_will_answer': get_user_model().objects.get(pk=1),
        })

        return context


class QuestionsList(TemplateView):
    template_name = 'question/questions_list.html'
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
            # rubrics_useful = rubric.get_children().filter(is_guide_rubric=True, is_question_rubric=False)
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
        filters_exclude = {}
        sort = []
        q = False
        query = ''
        query_string = ''
        tag = False
        current_url = reverse('questions:list')  # текущий url без параметров и страниц
        url_params = {}  # GET параметры для url, используется в пагинаторе
        cur_url_param = None  # Текущий url параметр для определиния активной ссылки в навигации

        # Вопросы
        if rubric:
            if rubric.keywords:
                query = '({})'.format(')|('.join(rubric.keywords.split("\n")))
                # sort.append('@relevance DESC')
            else:
                filters.update({'rubric_id': (rubric.pk,)})

            current_url = reverse('questions:list_rubric', kwargs={
                'rubric_slug': rubric.slug
            })

        if 'tag' in self.kwargs:
            try:
                tag = Tag.objects.get(slug=self.kwargs['tag'])
            except Tag.DoesNotExist:
                raise Http404
            query = self.kwargs['tag']
            sort.append('@relevance DESC')
            current_url = reverse('questions:list_tag', kwargs={
                'tag': kwargs['tag']
            })
            context.update({
                'tag': tag
            })

        if 'q' in self.request.GET:
            query = self.request.GET['q']
            sort.append('@relevance DESC')
            query_string = query
            url_params.update({
                'q': query,
            })

        if 'paid' in self.request.GET:
            filters.update({'is_pay': (True,)})
            url_params.update({
                'paid': True
            })
            cur_url_param = 'paid'

        if 'free' in self.request.GET:
            filters.update({'is_pay': (False,)})
            url_params.update({
                'free': True
            })
            cur_url_param = 'free'

        if 'unanswered' in self.request.GET:
            filters.update({'reply_count': (0,)})
            url_params.update({
                'unanswered': True
            })
            cur_url_param = 'unanswered'

        if 'lawyer' in self.request.GET:  # Вопросы с ответами юриста
            filters.update({'answers_authors_id': (int(self.request.GET['lawyer']),)})
            url_params.update({
                'lawyer': self.request.GET['lawyer']
            })
            cur_url_param = 'lawyer'

        if self.request.user.is_authenticated and self.request.user.is_lawyer():
            if 'my_advice' in self.request.GET:  # Вопросы с платными заявками юриста-эксперта
                filters.update({'advice_expert_id': (self.request.user.pk,)})
                url_params.update({
                    'my_advice': True
                })
                cur_url_param = 'my_advice'

            if 'additionals' in self.request.GET:
                filters.update({'additionals_user_id': (self.request.user.pk,)})
                url_params.update({
                    'additionals': True
                })
                cur_url_param = 'additionals'
        else:  # Вопросы клиента
            if 'my' in self.request.GET:
                filters.update({'author_id': (self.request.user.pk,)})
                url_params.update({
                    'my': True
                })
                cur_url_param = 'my'

        if not self.request.user.is_authenticated or self.request.user.is_client() or 'my' not in self.request.GET:
            # Для неавторизованный пользователей, и клиентов только вопросы с ответами
            filters_exclude.update({'reply_count': (0,)})
            print(self.request.user.is_client())

        if self.request.user.is_authenticated and self.request.user.is_lawyer() and 'my_advice' not in self.request.GET:
            # Для юристов, не показываем платные вопросы
            # Платные вопросы показываем только те,  которых юрист ведёт
            filters.update({'is_pay': (False,)})

        # filters.update({'answers_authors_id': (1,)})

        # QuerySet для списка вопросов
        question_set = Question.published.search(
            query=query,
            offset=start,
            limit=self.page_size,
            filters=filters,
            filters_exclude=filters_exclude,
            sort=sort,
        )

        context.update({
            'current_url': current_url,
            'url_params': "?" + urlencode(url_params) if url_params else '',
            'cur_url_param': cur_url_param,
            'total_found': question_set.count,
            'current_page': current_page,
            'next_page': current_page + 1 if current_page * self.page_size < question_set.count else None,
            'questions': question_set,
            'query_string': query_string,
        })

        # Списки рубрик для aside «Темы консультаций, рубрикатор» и «Консультируем так же»
        context.update({
            'rubrics_list': Rubric.objects.order_by('tree_id', 'id').filter(level__in=(0, 1,), is_question_rubric=True),
            'rubrics_also_list': rubrics_also_list,
            'rubrics_useful': rubrics_useful,
            # 'rubrics_list': Rubric.rubricator.filter(level__in=(0,)),
        })

        # Лучшие юристы блок
        context.update({
            'lawyers_from_rating': Rating.lawyers.filter(month_rate__gt=0)[:5]
        })

        h1 = 'Консультация юриста и адвоката онлайн'
        if rubric:
            h1 = rubric.h1 if rubric.h1 else rubric.title if rubric.title else rubric
        if tag:
            h1 = tag.name

        if not self.request.user.is_authenticated or self.request.user.role == 1:
            h2_begin = 'Юридические консультации'
            h2_end = 'по российскому законодательству'
        else:
            h2_begin = 'Вопросы'
            h2_end = 'юристу'

        if rubric:
            h2 = '{} по теме «{}»'.format(h2_begin, rubric.name)
        elif tag:
            h2 = '{} по теме «{}»'.format(h2_begin, tag.name)
        elif query_string:
            h2 = 'Результаты поиска'
        else:
            h2 = '{} {}'.format(h2_begin, h2_end)

        title = 'Консультации юристов и адвокатов на сайте Мойюрист.онлайн'
        if rubric:
            title = rubric.title if rubric.title else rubric.h1 if rubric.h1 else \
                    'Консультации юристов по теме «{}» на сайте Мойюрист.онлайн'.format(rubric.name)
        elif tag:
            title = 'Консультации юристов по теме «{}» на сайте Мойюрист.онлайн'.format(tag.name)
        elif query_string:
            title = 'Результаты поиска. Юридические консультации онлайн'

        context.update({
            'h1': h1,
            'h2': h2,
            'title': title,
        })

        return context


class AskQuestion(TemplateView):
    template_name = 'question/ask.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AskQuestion, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        # Данные с онлайн-консультанта
        data = {
            'ask_content': request.POST.get('question', request.POST.get('text', False)),
            'ask_name': request.POST.get('name', False),
        }
        data.update({
            'ask_phone': request.POST['code'] + request.POST['phone']
            if 'code' in request.POST and 'phone' in request.POST else False
        })

        request.session.update(data)

        return super(AskQuestion, self).render_to_response(context)


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
