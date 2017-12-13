from django.conf.urls import url

from .views import (
    QuestionCreateAPIView,
    QuestionDeleteAPIView,
    QuestionDetailAPIView,
    QuestionUpdateAPIView,
    QuestionListAPIView,
    AnswerDetailAPIView,
    AnswerListAPIView,
    AnswerUpdateAPIView,
    AnswerCreateAPIView,
)


app_name = 'entry_api'

urlpatterns = [
    url(r'^questions/$', QuestionListAPIView.as_view(), name='question-list'),
    url(r'^questions/create/$', QuestionCreateAPIView.as_view(), name='question-create'),
    url(r'^questions/(?P<pk>\d+)/$', QuestionDetailAPIView.as_view(), name='question-detail'),
    url(r'^questions/(?P<pk>\d+)/edit/$', QuestionUpdateAPIView.as_view(), name='question-update'),
    url(r'^questions/(?P<pk>\d+)/delete/$', QuestionDeleteAPIView.as_view(), name='question-delete'),

    url(r'^answers/$', AnswerListAPIView.as_view(), name='answer-list'),
    url(r'^answers/create/$', AnswerCreateAPIView.as_view(), name='answer-create'),
    url(r'^answers/(?P<pk>\d+)/$', AnswerDetailAPIView.as_view(), name='answer-detail'),
    url(r'^answers/(?P<pk>\d+)/edit/$', AnswerUpdateAPIView.as_view(), name='answer-update'),
]
