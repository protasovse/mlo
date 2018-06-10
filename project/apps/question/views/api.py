import os
import binascii

from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from phonenumbers import PhoneNumberFormat, format_number, parse

from apps.account.models import Subscription
from apps.advice.models import Advice
from apps.rating.models import Type, RatingScore, RatingScoreComment
from apps.rating.utils import add_score
from apps.review.models import Likes
from apps.svem_system.exceptions import ApiPublicException
from apps.svem_system.views.api import ApiView
from apps.entry.models import Question, Answer, Entry, Files, DEFAULT_RUBRIC
from django.contrib.auth import get_user_model
from apps.svem_auth.models import emails
from apps.entry.managers import BLOCKED
from apps.svem_auth.models.validators import CityIdValidator
import config.error_messages as err_txt
from django.contrib import messages
from config import flash_messages
from config.settings import ADVICE_COST, ANSWERS_TREE_IS_EXPANDED, ALL_PARTNER
from apps.entry.services import answer as to_answer, send_to_all_partner


class QuestionView(ApiView):
    @classmethod
    def get(cls, request, qid):
        q = Question.objects.filter(pk=qid).select_related(
            'author', 'author__city', 'author__info', 'author__rating'
        ).get()
        q_data = q.get_public_data()
        q_data.update({'is_can_answer': False})

        files = QuestionFilesView.get_files(request, q)
        q_data.update({'files': files[q.id] if files else False})
        return q_data

    @classmethod
    def post(cls, request, qid=0):
        if not qid:
            qid = request.POST['id']
        f = Question.objects.get(pk=qid).upload_document(request.FILES['file'])
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

        params['rubric_id'] = params.get('rubric[id]', DEFAULT_RUBRIC)

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

                # mail to lawyers
                for r in Subscription.objects.filter(rubrics__in=[q.rubric]):
                    print(r.user)
                    emails.send_new_question_to_expert(r.user, q)

                if ALL_PARTNER:  # Если влючена парнёрская программа — отправим заявку
                    send_to_all_partner(
                        name=params['name'],
                        phone=params['phone'][5:],
                        code=params['phone'][2:5],
                        question=params['content'],
                        ip=cls.get_client_ip(request)
                    )
        else:
            messages.add_message(
                request, messages.SUCCESS, flash_messages.QUESTION_CREATE_ACTIVE.format(id=q.id), 'success'
            )

        return {
            'id': q.id,
            'status': q.status
        }


class AnswersFilesView(ApiView):
    @classmethod
    def is_show(cls, entry_id, request, question, answers_authors):
        """
        определим фунцию которая будет возвращать флаг - показывать ли файл
        Хуевенькая передача параметров.
        :param entry_id:
        :param request:
        :param question:
        :param answers_authors:
        :return:
        """
        # не показываем файлы незалогиненому пользователю
        if not request.user.is_authenticated:
            return False
        # если текущий юзер автор вопроса - то все вложения ему видны
        if request.user.id == question.author.id:
            return True
        # если текущий юзер - юрист, ответивший на вопрос, то ему видны все вложения в его ветке
        if answers_authors[entry_id] == request.user.id:
            return True
        # во всех остальных случаях - не видны
        return False

    @classmethod
    def get_files(cls, request, answers, question):
        # для кажого ответа 2-ого уровня найдем ответ 1-ого уровня и возьмем его автора (юриста)
        answers_authors = {}
        author_id = None
        for a in answers:
            if a['parent_id'] is None:
                author_id = a['author']['id']
            answers_authors[a['id']] = author_id

        files = {}
        # найдем все файлы для ответов на вопрос question
        for f in Files.objects.filter(entry_id__in=[a['id'] for a in answers]):
            p_data = f.get_public_data(cls.is_show(f.entry_id, request, question, answers_authors))
            try:
                files[f.entry_id].append(p_data)
            except KeyError:
                files[f.entry_id] = [p_data]
        return files

    @classmethod
    def get(cls, request, qid, aid):
        question = Question.published.get(pk=qid)
        answers = Answer.published.related_to_question(question).filter(pk=aid)
        files = cls.get_files(request, [a.get_public_data() for a in answers], question)
        return files[aid] if files else []


class QuestionFilesView(ApiView):
    @classmethod
    def is_show(cls, request, question):
        """
        определим фунцию которая будет возвращать флаг - показывать ли файл
        :param request:
        :param question:
        :return:
        """
        # не показываем файлы незалогиненому пользователю
        if not request.user.is_authenticated:
            return False
        # если текущий юзер автор вопроса - то все вложения ему видны
        if request.user.id == question.author.id:
            return True
        # если текущий юзер - юрист, то ему видны все вложения в любом вопросе
        if request.user.is_lawyer:
            return True
        # во всех остальных случаях - не видны
        return False

    @classmethod
    def get_files(cls, request, question):
        files = {}
        # найдем все файлы для ответов на вопрос question
        for f in Files.objects.filter(entry_id=question.id):
            p_data = f.get_public_data(cls.is_show(request, question))
            try:
                files[f.entry_id].append(p_data)
            except KeyError:
                files[f.entry_id] = [p_data]
        return files


class AnswersView(ApiView):
    @classmethod
    def put(cls, request, qid):
        params = cls.get_put(request)
        question = Question.objects.get(pk=qid)
        answer = to_answer(question, params['content'], request.user, params['parent_id'])
        return answer.get_public_data()

    @classmethod
    def post(cls, request, qid):
        f = Answer.objects.get(pk=request.POST['id']).upload_document(request.FILES['file'])
        return 'file {} uploaded'.format(f.file)

    @classmethod
    def get(cls, request, qid):
        def _is_can_like(a, user, lks):
            if not user.is_authenticated:
                return {'is_can_like': False}
            if a['id'] not in lks.keys() and a['author']['id'] != user.id:
                return {'is_can_like': True}
            res = {'is_can_like': False}
            if a['id'] in lks.keys():
                res['my_like'] = lks[a['id']]
            return res

        question = Question.objects.get(pk=qid)
        if question.status != 'public':
            return []

        likes = {l.entry_id: l.value for l in
                 Likes.objects.filter(user_id=request.user.id, entry__answer__on_question=qid)
                 } if request.user.is_authenticated else {}

        answers = [a.get_public_data() for a in Answer.published.related_to_question(question)]

        files = AnswersFilesView.get_files(request, answers, question)

        # to prepare array of answers for front
        for i, a in enumerate(answers):
            a.update(_is_can_like(a, request.user, likes))
            if a['parent_id'] is None:
                a.update({'is_expand': ANSWERS_TREE_IS_EXPANDED})
            # add files to answers
            if a['id'] in files.keys():
                a.update({'files': files[a['id']]})
            else:
                a.update({'files': False})

            """
             to mark last answers in thread
            """
            # lawyer's answers are not mark
            if a['parent_id'] is None:
                a.update({'is_last_answer': False})
                continue
            try:
                n = answers[i + 1]
                a.update({'is_last_answer': a['parent_id'] != n['parent_id']})
            except IndexError:
                a.update({'is_last_answer': True})
        return answers


class BaseAnswersLike(ApiView):
    @classmethod
    def like(cls, request, aid, val):
        if not request.user.is_authenticated:
            raise ApiPublicException('access denied')
        answer = Answer.objects.select_related().get(pk=aid)

        if not answer.author.is_lawyer() or answer.author_id == request.user.id:
            raise ApiPublicException('access denied lawyer {}'.format(answer.author.role))
        if Likes.objects.filter(user_id=request.user.id, entry_id=answer.id).count() > 0:
            raise ApiPublicException('access denied')
        if val not in [1, -1]:
            raise ApiPublicException('data error')
        Likes.objects.create(entry=answer, user=request.user, value=val)
        Entry.objects.filter(pk=answer.id).update(like_count=F('like_count') + val)

        # добавляем балл рейтинга
        prefix = 'usefull' if val == 1 else 'useless'
        comment_prefix = 'Полезный' if val == 1 else 'Бесполезный'
        if request.user.is_lawyer():  # like ставит юрист
            type_key = '{}_answer_lawyer'.format(prefix)
        elif answer.on_question.author == request.user:  # like ставит клиент — автор вопроса
            type_key = '{}_answer_author_questions'.format(prefix)
        else:  # like ставит клиент за чужой вопрос
            type_key = '{}_answer_client'.format(prefix)
        rating_type = Type.objects.get(key=type_key)
        score = RatingScore.objects.create(user=answer.author, type=rating_type)
        RatingScoreComment.objects.create(rating_score=score, comment='{} ответ {}'.format(comment_prefix, answer.pk))
        add_score(answer.author_id, score.type.value)


class AnswersLike(BaseAnswersLike):
    @classmethod
    def post(cls, request, qid, aid):
        cls.like(request, aid, 1)


class AnswersDislike(BaseAnswersLike):
    @classmethod
    def post(cls, request, qid, aid):
        cls.like(request, aid, -1)


class QuestionDefault(ApiView):
    @classmethod
    def get(cls, request):
        return {
            'ask_content': request.session.pop('ask_content', ''),
            'ask_name': request.session.pop('ask_name', ''),
            'ask_phone': request.session.pop('ask_phone', ''),
        }


class WidgetSend(ApiView):

    @classmethod
    @csrf_exempt
    def post(cls, request):

        r = send_to_all_partner(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            code=request.POST.get('code'),
            question=request.POST.get('question'),
            ip=cls.get_client_ip(request),
        )
