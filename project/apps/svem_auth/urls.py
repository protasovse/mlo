from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth.views import logout
from apps.svem_auth.views.social_network import VK, FB

urlpatterns = [

    path('logout', logout, {'next_page': '/'}, name='logout'),
    path('vk', VK.as_view()),
    path('fb', FB.as_view()),
    re_path('^', TemplateView.as_view(template_name="svem_auth/index.html"), name='login'),
]

