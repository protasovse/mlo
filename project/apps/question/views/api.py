import os
import binascii
from apps.svem_system.views.api import ApiView
from apps.entry.models import Question
from django.contrib.auth import get_user_model
from apps.svem_auth.models import emails
from apps.entry.managers import BLOCKED, PUBLISHED


class QuestionView(ApiView):

    @classmethod
    def post(cls, request):
        f = Question.objects.get(pk=request.POST['id'])\
            .upload_document(request.FILES['file'])
        return 'file {} uploaded'.format(f.file)

    @classmethod
    def put(cls, request):
        """
        create a question. If user doesn't authorised - we will send email whith link to confirmation question
        if user exits - then we will found his by email
        :param request:
        :return:
        """
        params = cls.get_put(request)
        if request.user.is_authenticated:
            user = request.user
            status = PUBLISHED
        else:
            status = BLOCKED
            _email = params['email']
            try:
                user = get_user_model().objects.get(email=_email)
            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_user(
                    _email, binascii.hexlify(os.urandom(6)).decode(),
                    first_name=params['name'],
                    phone=params['phone'],
                )

        q = Question.objects.create(
            title=params['title'],
            content=params['content'],
            author_id=user.id,
            status=status,
            is_pay=params['is_paid_question']
        )
        q.rubrics.set(params.getlist('rubric[]'))
        if status == BLOCKED:
            emails.send_confirm_question(q)
        return {
            'id': q.id,
            'status': status
        }
