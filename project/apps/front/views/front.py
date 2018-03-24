from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.entry.models import Question
from apps.rating.models import Rating


class Mainpage(TemplateView):
    template_name = 'front/index.html'

    def get_context_data(self, **kwargs):
        context = super(Mainpage, self).get_context_data(**kwargs)
        context['h1'] = "Консультация юриста онлайн"

        context['questions'] = Question.published.filter(reply_count__gt=0).all()[:3]
        context['lawyers'] = Rating.objects.filter(month_rate__gt=0)[:15]

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


