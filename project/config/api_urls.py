from django.urls import path
from apps.svem_auth.views import api
from apps.rubric import view_api as rubric_api
from apps.question.views import api as question_api

urlpatterns = [
    path("user/check", api.CheckLogin.as_view()),
    path("user/flash", api.FlashMessageCheck.as_view()),
    path("user/forgot", api.ForgotPassword.as_view()),
    path("user/reset", api.ResetPassword.as_view()),
    path("user/activate", api.ActivateAccount.as_view()),
    path("user/resend", api.ReSend.as_view()),
    path("user", api.AppUser.as_view()),
    path('rubric', rubric_api.Rubrics.as_view()),
    path('question', question_api.Question.as_view())
]

