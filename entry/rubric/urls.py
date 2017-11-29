from django.conf.urls import url

from entry.rubric.views import RubricDetail

urlpatterns = [
    url(r'^(?P<slug>[а-яйё\-]+)/$', RubricDetail.as_view(), name='rubric-detail'),
]
