from django.urls import re_path
from apps.question.views.front import AskQuestion

urlpatterns = [
    re_path('', AskQuestion.as_view(), name='ask_question'),
]
