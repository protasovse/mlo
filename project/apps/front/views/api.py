from apps.svem_system.views.api import ApiView
from django.conf import settings
from django.urls import reverse


class FrontDefault(ApiView):
    @classmethod
    def get(cls, request):
        return {
            'settings': {
                'advice_cost':  settings.ADVICE_COST,
                'answers_expand': settings.ANSWERS_TREE_IS_EXPANDED,
                'site_url': settings.SITE_URL,
                'site_protocol': settings.SITE_PROTOCOL

            },
            'advice': {
                'money_yandex_purse': settings.MONEY_YANDEX_PURSE,
                'payment_form_title': settings.PAYMENT_FORM_TITLE,
                'payment_form_target': settings.PAYMENT_FORM_TARGET,
                'advice_cost': settings.ADVICE_COST,
            },
            'urls': {
                'show_question': reverse('question:detail', kwargs={'pk': 0}),
                'ask_question': reverse('ask_question'),
            }
        }
