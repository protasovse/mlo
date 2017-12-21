from django.shortcuts import render
from django.views.generic import TemplateView


class Mainpage(TemplateView):
    template_name = 'front/mainpage.html'

    def get_context_data(self, **kwargs):
        context = super(Mainpage, self).get_context_data(**kwargs)
        context['hui'] = "Хуй"
        return context

