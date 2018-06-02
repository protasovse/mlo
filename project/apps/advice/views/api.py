from apps.advice.models import Advice
from apps.svem_system.views.api import ApiView


class AdviceView(ApiView):

    @classmethod
    def get(cls, request, qid):
        advice = Advice.objects.filter(question_id=qid).get()
        return advice.get_public_data()


