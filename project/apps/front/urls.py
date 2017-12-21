from django.conf.urls import url

from apps.front.views import Mainpage

urlpatterns = [
    url(r'^$', Mainpage.as_view(), name='mainpage'),
]
