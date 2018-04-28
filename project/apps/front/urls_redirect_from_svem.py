from django.urls import re_path

from apps.front.views import redirect_from_svem
from apps.front.views.redirect_from_svem import Redirect

urlpatterns = [
    # /Trudovoe-pravo/253-trudovoe-pravo/
    re_path(r'^[\w-]+/\d+-[\w-]+/$', redirect_from_svem.red),
    # /Trudovoe-pravo/253-trudovoe-pravo/294226-pochemu-iz-moej-zarplaty-vychli-otpusknye/
    re_path(r'^[\w-]+/\d+-[\w-]+/(?P<question_id>\d+)-[\w-]+/$', redirect_from_svem.tag),
    # re_path(r'^[\w-]+/\d+-\w+\(?P<question_id>\d+-\w+)/$', Redirect.as_view()),
]