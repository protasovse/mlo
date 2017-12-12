from django.conf.urls import url

from entry.views import QuestionDetail


app_name = 'entry'
urlpatterns = [
    url(r'^(?P<pk>[\d]+)/$', QuestionDetail.as_view(), name='detail'),
]
