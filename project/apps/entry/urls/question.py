from django.urls import path
from apps.question.views.front import ConfirmQuestion
from apps.entry.views import QuestionDetail
app_name = 'entry'

urlpatterns = [
    path('<int:pk>/', QuestionDetail.as_view(), name='detail'),
    path('<int:pk>/<slug:token>', ConfirmQuestion.as_view(), name='confirm_q'),
]
