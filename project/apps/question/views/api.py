import os
import binascii
from phonenumbers import PhoneNumberFormat, format_number, parse
from apps.svem_system.views.api import ApiView
from apps.entry.models import Question
from django.contrib.auth import get_user_model
from apps.svem_auth.models import emails
from apps.entry.managers import BLOCKED, PUBLISHED
from apps.svem_auth.models.validators import CityIdValidator
import config.error_messages as err_txt
from apps.svem_auth.models.users import UserHash
from django.contrib import messages
from django.urls import reverse


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
        phone_number = format_number(parse(params['phone'], 'RU'), PhoneNumberFormat.E164) if params['phone'] else None
        city_id = params['city[id]'] if 'city[id]' in params.keys() else False
        if request.user.is_authenticated:
            user = request.user
            status = PUBLISHED
        else:
            status = BLOCKED
            _email = params['email']
            try:
                user = get_user_model().objects.get(email=_email)
            except get_user_model().DoesNotExist:

                if int(city_id):
                    city_validator = CityIdValidator(err_txt.MSG_CITY_DOESNT_EXISTS, 'city')
                    city_validator(city_id)
                else:
                    city_id = None
                user = get_user_model().objects.create_user(
                    _email, binascii.hexlify(os.urandom(6)).decode(),
                    first_name=params['name'],
                    phone=phone_number,
                    city_id=city_id
                )

        token = UserHash.get_or_create(user) if status == BLOCKED else None

        q = Question.objects.create(
            title=params['title'],
            content=params['content'],
            author_id=user.id,
            status=status,
            is_pay=params['is_paid_question'],
            key=token,
            first_name=params['name'] if params['name'] else user.first_name,
            phone=phone_number,
            city_id=user.city_id if user.city_id else city_id
        )
        q.rubrics.set(params.getlist('rubric[]'))
        if status == BLOCKED:
            emails.send_confirm_question(user, q, token)
            messages.add_message(
                request,
                messages.WARNING,
                '<h4>Ваш вопрос принят</h4>'
                '<p>Но он пока не виден юристам. Для публикации вопроса, подтвердите ваш электронный ящик, '
                'кликнув по ссылки в отправленном письме.</p>',
                'danger'
            )
            # add question_id to session
            question_ids = request.session.get('question_ids', [])
            question_ids.append(q.id)
            request.session['question_ids'] = question_ids
        else:
            messages.add_message(
                request,
                messages.SUCCESS,
                '<h4>Подтверждён и опубликован</h4>'
                '<p>Вопросу присвоен номер {id}, и он будет доступен по ссылке: http://мойюрист.онлайн/{url}/</p>'
                '<p>Вопрос будет находиться на рассмотрении в течение 7 дней, если к концу этого периода ответ не '
                'поступит, то он больше не будет рассматриваться юристами.</p>'.format(id=q.id, url=reverse('question:detail', kwargs={'pk': 0})),
                'success'
            )

        return {
            'id': q.id,
            'status': status
        }
