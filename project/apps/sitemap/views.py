from django.contrib.sitemaps import Sitemap
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView


class StaticSitemap(Sitemap):
    priority = 0.5  # Приоритет
    changefreq = 'daily'  # Частота проверки

    # Метод, возвращающий массив с url-ками
    def items(self):
        return ['front:terms_of_use', 'front:about']

    # Метод непосредственной экстракции url из шаблона
    def location(self, item):
        return reverse(item)

'''
class Sitemap(TemplateView):
    template_name = 'sitemap/urls.xml'
    content_type = 'application/xml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'now': timezone.now(),
        })
        return context


class Pages(Sitemap):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'urls': (
            '/',
            '/вопросы/',
        )})
        return context
'''
