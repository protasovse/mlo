import os
import binascii
from phonenumbers import PhoneNumberFormat, format_number, parse
from apps.svem_system.views.api import ApiView
from apps.entry.models import Question
from django.contrib.auth import get_user_model
from apps.svem_auth.models import emails
from apps.entry.managers import BLOCKED
from apps.svem_auth.models.validators import CityIdValidator
import config.error_messages as err_txt
from django.contrib import messages
from config import flash_messages


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
        params = params.dict()
        phone = format_number(parse(params['phone'], 'RU'), PhoneNumberFormat.E164) \
            if params['phone'] else None
        params['phone'] = phone
        city_id = params['city[id]'] if 'city[id]' in params.keys() else None
        params['city_id'] = int(city_id) or None
        if params['city_id']:
            city_validator = CityIdValidator(err_txt.MSG_CITY_DOESNT_EXISTS, 'city')
            city_validator(params['city_id'])

        if request.user.is_authenticated:
            user = request.user
        else:
            try:
                user = get_user_model().objects.get(email=params['email'])
            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_user(
                    params['email'], binascii.hexlify(os.urandom(6)).decode(),
                    first_name=params['name'],
                    phone=params['phone'],
                    city_id=params['city_id']
                )

        if int(params['is_paid_question']) == 1:
            q = Question.objects.create_paid_question(user, params)
        else:
            q = Question.objects.create_free_question(user, params)
        q.rubrics.set(cls.get_put(request).getlist('rubric[]'))

        if q.status == BLOCKED:
            # add question_id to session
            question_ids = request.session.get('question_ids', [])
            question_ids.append(q.id)
            request.session['question_ids'] = question_ids

            if q.is_pay:
                emails.send_paid_question(user, q)
            else:
                emails.send_confirm_question(user, q, q.token)
                messages.add_message(request, messages.WARNING, flash_messages.QUESTION_CREATE_BLOCKED, 'danger')
        else:
            messages.add_message(
                request, messages.SUCCESS, flash_messages.QUESTION_CREATE_ACTIVE.format(id=q.id), 'success'
            )

        return {
            'id': q.id,
            'status': q.status
        }
