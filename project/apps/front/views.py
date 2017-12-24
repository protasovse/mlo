from django.shortcuts import render
from django.views.generic import TemplateView


class Mainpage(TemplateView):
    template_name = 'front/index.html'

    def get_context_data(self, **kwargs):
        context = super(Mainpage, self).get_context_data(**kwargs)
        context['h1'] = "Консультация юриста онлайн"
        return context

