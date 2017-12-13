from django.conf.urls import url

from apps.rubric.views import RubricDetail

app_name = 'rubric'
urlpatterns = [
    url(r'^(?P<slug>[а-яйё\-]+)/$', RubricDetail.as_view(), name='rubric-detail'),
]
