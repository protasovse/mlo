from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth import login
from apps.svem_auth.models.users import UserHash
from apps.entry.models import Question
from apps.entry.managers import PUBLISHED
from django.contrib import messages
from django.urls import reverse
from datetime import date
from apps.svem_system.exceptions import ControlledException


class AskQuestion(TemplateView):
    template_name = 'question/ask.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        mess = messages.get_messages(self.request)
        if len(mess) == 0:
            return kwargs
        for message in mess:
            # There is not method of taking first element. Why?)
            if message.level == messages.ERROR:
                kwargs.update({
                    'mess': message.message
                })

        return kwargs


class ConfirmQuestion(RedirectView):
    def get_redirect_url(self, **kwargs):
        try:
            pk = kwargs['pk']
            token = kwargs['token']
            hash_obj = UserHash.objects.get(key=token)
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
            messages.add_message(self.request, messages.ERROR, 'Не удалось подтвердить вопрос')
            return reverse('question:detail', kwargs={'pk': kwargs['pk']})

