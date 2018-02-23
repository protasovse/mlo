from django.urls import path

from apps.entry.views import QuestionDetail
app_name = 'entry'

urlpatterns = [
    path('<int:pk>/', QuestionDetail.as_view(), name='detail'),
]
