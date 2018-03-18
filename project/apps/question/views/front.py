from django.views.generic.base import TemplateView, RedirectView
from apps.svem_auth.models.users import UserHash
from apps.entry.models import Question
from apps.entry.managers import BLOCKED, PUBLISHED
from django.contrib import messages
from django.urls import reverse
from datetime import date


class AskQuestion(TemplateView):
    template_name = 'question/ask.html'


class ConfirmQuestion(RedirectView):

    def get_redirect_url(self, **kwargs):
        try:
            token = kwargs['token']
            hash_obj = UserHash.objects.get(key=token)
            # if hash exists, but too late
            if hash_obj.live_until.date() < date.today():
                messages.add_message(self.request, messages.ERROR, 'Не удалось подтвердить вопрос')
                return reverse('ask_question')
            user = hash_obj.user
            # if user doesnt active
            user.activate(True)
            # do activate question
            q = Question.objects.get(key=token)
            q.status = PUBLISHED
            q.save()
            hash_obj.delete()
        except UserHash.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, 'Не удалось подтвердить вопрос')
            return reverse('ask_question')

