from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth import login

from apps.advice.models import Advice, ADVICE_PAYMENT_CONFIRMED, ADVICE_INWORK
from apps.advice.settings import ADVICE_OVERDUE_TIME
from apps.rating.models import Rating
from apps.svem_auth.models.users import UserHash
from apps.entry.models import Question, Answer
from apps.entry.managers import PUBLISHED
from django.contrib import messages
from django.urls import reverse
from datetime import date, timedelta
from apps.svem_system.exceptions import ControlledException


class QuestionDetail(TemplateView):
    template_name = 'question/question_detail.html'

    def get_context_data(self, **kwargs):
        context = {}

        question = Question.published.get(pk=kwargs['pk'])

        context.update({
            'question': question
        })

        if question.is_pay:
            advice = Advice.objects.get(question=question)
            advice_context = {
                'advice': advice
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
            'answers': Answer.published.related_to_question(question)
        })

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

            q.status = PUBLISHED
            q.save()

            user = hash_obj.user
            # if user doesnt active
            user.activate(True)

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
