from django.conf.urls import url
from django.urls import path

from apps.front.views import Mainpage, LawyerPage, AskQuestion

urlpatterns = [
    url(r'^$', Mainpage.as_view(), name='mainpage'),

    path('юрист/<int:id>/', LawyerPage.as_view(), name='lawyer_page'),
    path('задать-вопрос/', AskQuestion.as_view(), name='ask_question'),
]
