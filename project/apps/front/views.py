from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from apps.account.models import Info, Contact, RatingResult
from apps.entry.models import Question
from apps.svem_system.views.api import ApiView


class Mainpage(TemplateView):
    template_name = 'front/index.html'

    def get_context_data(self, **kwargs):
        context = super(Mainpage, self).get_context_data(**kwargs)
        context['h1'] = "Консультация юриста онлайн"

        context['questions'] = Question.published.all()[:3]
        context['lawyers'] = RatingResult.objects.all().order_by('-value')[:5]

        return context


class LawyerPage(TemplateView):
    template_name = 'front/lawyer_page.html'

    def get_context_data(self, **kwargs):
        context = super(LawyerPage, self).get_context_data(**kwargs)

        lawyer = get_object_or_404(get_user_model(), pk=kwargs['id'])
        # lawyer_info = Info.objects.filter(user=lawyer)
        # lawyer_contact = Contact.objects.filter(user=lawyer)

        context['lawyer'] = lawyer
        # context['lawyer_info'] = lawyer_info if lawyer_info is None else None
        # context['lawyer_contact'] = lawyer_contact

        return context


class AskQuestion(TemplateView):

    template_name = 'front/ask_question.html'

    def get_context_data(self, **kwargs):
        context = super(AskQuestion, self).get_context_data(**kwargs)
        return context

    def post(self, request):
        pass