from apps.svem_system.views.api import ApiView
from django.conf import settings
from django.urls import reverse


class FrontDefault(ApiView):
    @classmethod
    def get(cls, request):
        return {
            'settings': {
                'advice_cost':  settings.ADVICE_COST
            },
            'urls': {
                'show_question': reverse('question:detail', kwargs={'pk': 0})
            }
        }
