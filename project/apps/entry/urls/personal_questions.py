from django.urls import path, re_path

from apps.entry.views import QuestionsFeedList
app_name = 'entry'

urlpatterns = [
    re_path('((?P<page>\d+)/)?', QuestionsFeedList.as_view(), name='list'),
]