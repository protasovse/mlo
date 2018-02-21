from django.conf.urls import url

from apps.entry.views import QuestionDetail

app_name = 'entry'
urlpatterns = [
    url(r'^(?P<pk>[\d]+)/$', QuestionDetail.as_view(), name='detail'),
]
