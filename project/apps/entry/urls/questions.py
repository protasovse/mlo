from django.urls import path, re_path

from apps.question.views.front import QuestionsList

app_name = 'entry'

urlpatterns = [
    path('', QuestionsList.as_view(), name='list'),
    path('<str:rubric_slug>/', QuestionsList.as_view(), name='list_rubric'),
    # path('<str:rubric_slug>/<str:subrubric_slug>/', QuestionsList.as_view(), name='list_subrubric'),
    path('<int:page>/', QuestionsList.as_view(), name='list'),
]
