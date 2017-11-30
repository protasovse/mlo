from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from base.mlo_auth.api.serializers import UserSerializer
from base.mlo_auth.managers import LAWYER
from ..models import Question, Answer

CONTENT_MIN_LEN = 15


class QuestionCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'title',
            'content',
            'pub_date',
            'rubrics',
        ]


question_detail_url = HyperlinkedIdentityField(
    view_name='questions:detail',
    lookup_field='pk',
)

question_detail_api_url = HyperlinkedIdentityField(
    view_name='entries-api:question-detail',
    lookup_field='pk',
)

answer_detail_api_url = HyperlinkedIdentityField(
    view_name='entries-api:answer-detail',
    lookup_field='pk',
)


class QuestionDetailSerializer(ModelSerializer):
    url = question_detail_url
    api_url = question_detail_api_url
    author = SerializerMethodField()
    # image = SerializerMethodField()
    replies = SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id',
            'url',
            'api_url',
            'pk',
            'author',
            'title',
            'content',
            'html_content',
            'pub_date',
            'reply_count',
            'replies',
        ]

    def get_author(self, obj):
        return UserSerializer(obj.author, context=self.context).data

    @staticmethod
    def get_html_content(obj):
        return obj.html_content

    def get_replies(self, obj):
        a_qs = Answer.answers.by_question(obj.id)
        answers = AnswerDetailSerializer(a_qs, context=self.context, many=True).data
        return answers


class QuestionListSerializer(ModelSerializer):
    url = question_detail_url
    api_url = question_detail_api_url
    author = SerializerMethodField()

    delete_url = HyperlinkedIdentityField(
        view_name='entries-api:question-delete',
        lookup_field='pk'
    )

    # rubrics = HyperlinkedRelatedField(view_name='rubrics:rubric-detail', read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'url',
            'api_url',
            'author',
            'title',
            'content',
            'rubrics',
            'pub_date',
            'delete_url',
            'reply_count',
        ]

    def get_author(self, obj):
        return UserSerializer(obj.author, context=self.context).data


class AnswerUpdateSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'content',
            'pub_date',
        ]


def answer_create_serializer(question_id=None, answer_id=None, author=None):
    class AnswerCreateSerializer(ModelSerializer):
        class Meta:
            model = Answer
            fields = [
                'id',
                'content',
                'pub_date',
            ]

        def __init__(self, *args, **kwargs):

            self.question_id = question_id
            self.author = author

            try:
                answer_parent_qs = Answer.answers.get(pk=answer_id)
                # Если задан answer_id для вопроса не 1-го уровня
                if not answer_parent_qs.is_parent:
                    answer_parent_qs = Answer.answers.get(pk=answer_parent_qs.parent.pk)
                self.parent_obj = answer_parent_qs
                # Если задан parent_obj, то номер вопроса берём из его entry_id и игнорируем question_id,
                # т.е. если ответ не 1-го уровня, то question_id можем и не задавать
                self.question_id = answer_parent_qs.entry_id
            except Answer.DoesNotExist:
                self.parent_obj = None

            super(AnswerCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):

            question_id = self.question_id

            if question_id is None:
                raise ValidationError(_('Установите номер вопроса (question_id) или номер ответа (answer_id), '
                                        'на которых на который нужно добавить комментарий.'))

            try:
                question = Question.published.get(pk=question_id)
            except Question.DoesNotExist:
                raise ValidationError(_('Вопрос с question_id = %s не существует или удалён.' % (question_id,)))

            # Для ответа 1-го уровня. Только юрист может его добавить и только один ответ.
            if self.parent_obj is None:

                if hasattr(self.author, 'role') is False or self.author.role != LAWYER:
                    raise ValidationError(_('Только юрист может отвечать на вопрос.'))

                if Answer.answers.by_question(question_id=question_id).filter(author=author).count() > 0:
                    raise ValidationError(_('Вы уже отвечали на этот вопрос.'))
            else:
                # Ответ 2-го уровня (комментарий на ответ) может добавить или автор вопроса, или любой юрист
                if question.author != self.author and \
                   (hasattr(self.author, 'role') is False or self.author.role != LAWYER):
                    raise ValidationError(_('Только юрист или автор вопроса может добавить комментарий к ответу.'))

            if len(data['content']) < CONTENT_MIN_LEN:
                raise ValidationError(_('Текст записи слишком короткий.'))

            return data

        def create(self, validated_data):
            content = validated_data.get('content')
            question_id = self.question_id
            parent_obj = self.parent_obj

            comment = Answer.answers.create(question_id, content, author, parent_obj)

            return comment

    return AnswerCreateSerializer


class AnswerDetailSerializer(ModelSerializer):
    api_url = answer_detail_api_url
    author = SerializerMethodField()
    replies = SerializerMethodField()

    class Meta:
        model = Answer
        fields = [
            'pk',
            'api_url',
            'author',
            'content',
            'html_content',
            'pub_date',
            'status',
            'parent',
            'reply_count',
            'replies',
        ]

    def get_author(self, obj):
        return UserSerializer(obj.author, context=self.context).data

    def get_html_content(self, obj):
        return obj.html_content

    def get_replies(self, obj):
        if obj.is_parent:
            return AnswerChildSerializer(obj.children(), context=self.context, many=True).data
        return None


class AnswerChildSerializer(ModelSerializer):
    api_url = answer_detail_api_url
    author = SerializerMethodField()

    class Meta:
        model = Answer
        fields = [
            'pk',
            'api_url',
            'author',
            'content',
            'html_content',
            'pub_date',
            'status',
        ]

    def get_author(self, obj):
        return UserSerializer(obj.author, context=self.context).data


class AnswerListSerializer(ModelSerializer):
    api_url = answer_detail_api_url
    author = SerializerMethodField()
    parent = HyperlinkedRelatedField(
        view_name='entries-api:answer-detail',
        read_only=True
    )

    class Meta:
        model = Answer
        fields = [
            'pk',
            'api_url',
            'author',
            'content',
            'html_content',
            'pub_date',
            'status',
            'parent',
            'reply_count',
        ]

    def get_author(self, obj):
        return UserSerializer(obj.author, context=self.context).data

    def get_html_content(self, obj):
        return obj.html_content
