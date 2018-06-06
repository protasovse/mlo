from apps.advice.models import Advice
from apps.svem_system.exceptions import ApiPublicException, ApiPrivateException
from apps.svem_system.views.api import ApiView


class AdviceView(ApiView):
    @classmethod
    def get(cls, request, qid):
        advice = Advice.objects.filter(question_id=qid).get()
        return advice.get_public_data()


class AdviceReject(ApiView):
    @classmethod
    def post(cls, request, qid, adid):
        advice = Advice.objects.filter(question_id=qid).filter(pk=adid).get()
        # отклонить advice может только тот, кому она назначена
        if advice.expert_id != request.user.id:
            raise ApiPublicException('access denied')
        result = advice.appoint_expert()
        if not result:
            raise ApiPrivateException('anything wrong')


class AdviceApprove(ApiView):
    @classmethod
    def post(cls, request, qid, adid):
        advice = Advice.objects.filter(question_id=qid).filter(pk=adid).get()
        # согласиться advice может только тот, кому она назначена
        if advice.expert_id != request.user.id:
            raise ApiPublicException('access denied')
        result = advice.to_in_work(request.POST.get('hours'))
        if not result:
            raise ApiPrivateException('anything wrong')


class AdviceConfirm(ApiView):
    @classmethod
    def post(cls, request, qid, adid):
        advice = Advice.objects.filter(question_id=qid).filter(pk=adid).select_related().get()
        # решить advice может только тот, кто автор вопроса
        if advice.question.author_id != request.user.id:
            raise ApiPublicException('access denied')
        result = advice.to_closed()
        if not result:
            raise ApiPrivateException('anything wrong')
