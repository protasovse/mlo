from django.urls import re_path, path
from apps.question.views.front import ConfirmQuestion, AskQuestion

urlpatterns = [
    path('<slug:token>', ConfirmQuestion.as_view(), name='confirm_q'),
    path('', AskQuestion.as_view(), name='ask_question'),
]
