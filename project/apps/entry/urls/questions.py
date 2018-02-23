from django.urls import path, re_path

from apps.entry.views import QuestionsList
app_name = 'entry'

urlpatterns = [
    re_path('((?P<page>\d+)/)?', QuestionsList.as_view(), name='list'),
]
