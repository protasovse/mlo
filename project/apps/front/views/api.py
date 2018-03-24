from apps.svem_system.views.api import ApiView
from django.urls import reverse


class FrontDefault(ApiView):
    @classmethod
    def get(cls, request):
        return {
            'urls': {
                'show_question': reverse('question:detail', kwargs={'pk': 0})
            }
        }
