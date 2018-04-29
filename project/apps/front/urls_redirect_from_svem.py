from django.urls import re_path

from apps.front.views import redirect_from_svem
from apps.front.views.redirect_from_svem import Redirect

urlpatterns = [
    # /Trudovoe-pravo/ — рубрика или /Trudovoe-pravo/0-vse/
    re_path(r'^(?P<rubric_slug2>[A-Z]+[\w-]+)/$', redirect_from_svem.rubric),
    re_path(r'^(?P<rubric_slug2>[A-Z]+[\w-]+)/0-vse/$', redirect_from_svem.rubric),
    # /Trudovoe-pravo/253-trudovoe-pravo/
    re_path(r'^[A-Z]+[\w-]+/(?P<tag_id>\d+)-[\w-]+/$', redirect_from_svem.tag),
    # /Trudovoe-pravo/253-trudovoe-pravo/294226-pochemu-iz-moej-zarplaty-vychli-otpusknye/
    re_path(r'^[A-Z]+[\w-]+/\d+-[\w-]+/(?P<question_id>\d+)-[\w-]+/$', redirect_from_svem.question),
]