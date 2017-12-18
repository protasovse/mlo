from django.urls import path
from apps.svem_auth.views import api

urlpatterns = [
    path("user/check", api.CheckLogin.as_view()),
    path("user/flash", api.FlashMessageCheck.as_view()),
    path("user/forgot", api.ForgotPassword.as_view()),
    path("user/reset", api.ResetPassword.as_view()),
    path("user/activate", api.ActivateAccount.as_view()),
    path("user/resend", api.ReSend.as_view()),
    path("user", api.AppUser.as_view()),
]

