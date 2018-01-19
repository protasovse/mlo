from django.conf.urls import url

from apps.front.views import Mainpage, LawyerPage

urlpatterns = [
    url(r'^$', Mainpage.as_view(), name='mainpage'),

    url(r'^юрист/(\d+)/$', LawyerPage.as_view(), name='lawyer_page'),
]
