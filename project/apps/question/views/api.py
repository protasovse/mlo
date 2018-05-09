import os
import binascii
from django.db.models import F
from phonenumbers import PhoneNumberFormat, format_number, parse
from apps.advice.models import Advice
from apps.review.models import Likes
from apps.svem_system.exceptions import ApiPublicException
from apps.svem_system.views.api import ApiView
from apps.entry.models import Question, Answer, Entry
from django.contrib.auth import get_user_model
from apps.svem_auth.models import emails
from apps.entry.managers import BLOCKED
from apps.svem_auth.models.validators import CityIdValidator
import config.error_messages as err_txt
from django.contrib import messages
from config import flash_messages
from config.settings import ADVICE_COST, ANSWERS_TREE_IS_EXPANDED


class QuestionView(ApiView):
    @classmethod
    def get(cls, request):
        return Question.objects.filter(pk=request.GET['id']).select_related(
            'author', 'author__city', 'author__info', 'author__rating'
        ).get().get_public_data()


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

        params['rubric_id'] = params.get('rubric[id]', None)

        password = '********'

        if params['city_id']:
            city_validator = CityIdValidator(err_txt.MSG_CITY_DOESNT_EXISTS, 'city')
            city_validator(params['city_id'])

        is_authenticated = False
        if request.user.is_authenticated:
            user = request.user
            is_authenticated = True
        else:
            try:
                user = get_user_model().objects.get(email=params['email'])
            except get_user_model().DoesNotExist:
                password = binascii.hexlify(os.urandom(8)).decode()
                user = get_user_model().objects.create_user(
                    params['email'], password,
                    first_name=params['name'],
                    phone=params['phone'],
                    city_id=params['city_id'],
                )

        if int(params['is_paid_question']) == 1:
            q = Question.objects.create_paid_question(user, params)
            Advice.objects.create(question=q, cost=ADVICE_COST)
        else:
            q = Question.objects.create_free_question(user, is_authenticated, params)

        if q.status == BLOCKED:
            # add question_id to session
            question_ids = request.session.get('question_ids', [])
            question_ids.append(q.id)
            request.session['question_ids'] = question_ids

            if q.is_pay:
                emails.send_paid_question(user, q, user.email, password)
            else:
                emails.send_confirm_question(user, q, q.token, user.email, password)
        else:
            messages.add_message(
                request, messages.SUCCESS, flash_messages.QUESTION_CREATE_ACTIVE.format(id=q.id), 'success'
            )

        return {
            'id': q.id,
            'status': q.status
        }


class AnswersView(ApiView):
    @classmethod
    def get(cls, request):
        def _is_can_like(a, user, lks):
            if not user.is_authenticated:
                return {'is_can_like': False}
            if not a['parent_id'] \
                    and a['id'] not in lks \
                    and a['author']['id'] != user.id:
                return {'is_can_like': True}
            return {'is_can_like': False}

        question = Question.objects.get(pk=request.GET['id'])
        if question.status != 'public':
            return []

        likes = [l.entry_id for l in
                 Likes.objects.filter(user_id=request.user.id, entry__answer__on_question=request.GET['id'])
                 ] if request.user.is_authenticated else []

        answers = [a.get_public_data() for a in Answer.published.related_to_question(question)]

        for i, a in enumerate(answers):
            a.update(_is_can_like(a, request.user, likes))
            if a['parent_id'] is None:
                a.update({'is_expand': ANSWERS_TREE_IS_EXPANDED})
            """
             to mark last answers in thread
            """
            # lawyer's answers are not mark
            if a['parent_id'] is None:
                a.update({'is_last_answer': False})
                continue
            try:
                n = answers[i+1]
                a.update({'is_last_answer': a['parent_id'] != n['parent_id']})
            except IndexError:
                a.update({'is_last_answer': True})

        return answers


class AnswersLike(ApiView):
    @classmethod
    def post(cls, request):
        if not request.user.is_authenticated:
            raise ApiPublicException('access denied')
        answer = Answer.objects.get(pk=request.POST['id'])
        if answer.parent_id or answer.author_id == request.user.id:
            raise ApiPublicException('access denied')
        if Likes.objects.filter(user_id=request.user.id, entry_id=answer.id).count() > 0:
            raise ApiPublicException('access denied')
        val = int(request.POST['value'])
        if val not in [1, -1]:
            raise ApiPublicException('data error')
        Likes.objects.create(entry=answer, user=request.user, value=val)
        Entry.objects.filter(pk=answer.id).update(like_count=F('like_count')+val)


class QuestionDefault(ApiView):
    @classmethod
    def get(self, request):
        return {
            'ask_content': request.session.pop('ask_content', ''),
            'ask_name': request.session.pop('ask_name', ''),
            'ask_phone': request.session.pop('ask_phone', ''),
        }
