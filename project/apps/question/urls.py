from django.urls import path
from apps.question.views.front import ConfirmQuestion, QuestionDetail
app_name = 'question'

urlpatterns = [
    path('<int:pk>/', QuestionDetail.as_view(), name='detail'),
    path('<int:pk>/<slug:token>', ConfirmQuestion.as_view(), name='confirm_q'),
]
