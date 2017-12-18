from django.conf.urls import url
from django.urls import path

from apps.rubric.views import RubricDetail, Index


app_name = 'rubric'
urlpatterns = [
    url(r'^(?P<slug>[а-яйё\-]+)/$', RubricDetail.as_view(), name='rubric-detail'),
    url(r'^(?P<slug>[а-яйё\-]+)/$', RubricDetail.as_view(), name='rubric-detail'),
    path('', Index.as_view())
]
