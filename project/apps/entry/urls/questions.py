from django.urls import path

from apps.question.views.front import QuestionsList

app_name = 'entry'

urlpatterns = [
    path('', QuestionsList.as_view(), name='list'),
    path('<int:page>/', QuestionsList.as_view(), name='list'),
    path('<str:rubric_slug>/', QuestionsList.as_view(), name='list_rubric'),
    path('<str:rubric_slug>/<int:page>/', QuestionsList.as_view(), name='list_rubric'),
    path('тема/<str:tag>/', QuestionsList.as_view(), name='list_tag'),
    path('тема/<str:tag>/<int:page>/', QuestionsList.as_view(), name='list_tag'),
    # path('<str:rubric_slug>/<str:subrubric_slug>/', QuestionsList.as_view(), name='list_subrubric'),
]
