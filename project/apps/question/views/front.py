from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import DetailView
from django.contrib.auth import login
from apps.svem_auth.models.users import UserHash
from apps.entry.models import Question, Answer
from apps.entry.managers import PUBLISHED
from django.contrib import messages
from django.urls import reverse
from datetime import date
from apps.svem_system.exceptions import ControlledException


class QuestionDetail(DetailView):
    template_name = 'question/question_detail.html'
    queryset = Question.published.all()
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context.update({
            'mess': messages.get_messages(self.request),
            'answers': Answer.published.by_question(context['object']).filter(parent_id=None)
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

