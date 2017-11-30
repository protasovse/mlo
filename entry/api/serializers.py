from django.urls import reverse
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from base.mlo_auth.api.serializers import UserSerializer
from base.mlo_auth.managers import LAWYER
from ..models import Question, Answer


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
        a_qs = Answer.answers.answers_by_question(obj.id)
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


def answer_create_serializer(question_id=None, parent_id=None, user=None):
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

            try:
                parent_qs = Answer.answers.get(pk=parent_id)
                self.parent_obj = parent_qs
            except Answer.DoesNotExist:
                self.parent_obj = None

            super(AnswerCreateSerializer, self).__init__(*args, **kwargs)

        def create(self, validated_data):
            content = validated_data.get('content')
            entry_id = self.question_id
            parent_obj = self.parent_obj
            comment = Answer.objects.create(
                content=content,
                entry_id=entry_id,
                parent=parent_obj,
                author=user,
            )
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
