from django.urls import path, re_path
from apps.front.views import api as front_api
from apps.svem_auth.views import api as auth_api
from apps.rubric import view_api as rubric_api
from apps.question.views import api as question_api
from apps.advice.views import api as advice_api
from apps.sxgeo.views import api as sxgeo_api

urlpatterns = [
    path("default", front_api.FrontDefault.as_view()),
    path("user/check", auth_api.CheckLogin.as_view()),
    path("user/flash", auth_api.FlashMessageCheck.as_view()),
    path("user/forgot", auth_api.ForgotPassword.as_view()),
    path("user/reset", auth_api.ResetPassword.as_view()),
    path("user/activate", auth_api.ActivateAccount.as_view()),
    path("user/resend", auth_api.ReSend.as_view()),
    path("user", auth_api.AppUser.as_view()),
    path('rubric', rubric_api.Rubrics.as_view()),
    path('questions/default', question_api.QuestionDefault.as_view()),
    path('questions', question_api.QuestionView.as_view()),
    path('questions/<int:qid>', question_api.QuestionView.as_view()),
    path('questions/<int:qid>/advice', advice_api.AdviceView.as_view()),
    path('questions/<int:qid>/advice/<int:adid>/reject', advice_api.AdviceReject.as_view()),
    path('questions/<int:qid>/advice/<int:adid>/approve', advice_api.AdviceApprove.as_view()),
    path('questions/<int:qid>/advice/<int:adid>/confirm', advice_api.AdviceConfirm.as_view()),
    path('questions/<int:qid>/answers/<int:aid>/like', question_api.AnswersLike.as_view()),
    path('questions/<int:qid>/answers/<int:aid>/dislike', question_api.AnswersDislike.as_view()),
    path('questions/<int:qid>/answers', question_api.AnswersView.as_view()),
    path('questions/<int:qid>/answers/<int:aid>/files', question_api.AnswersFilesView.as_view()),
    path('city/search', sxgeo_api.City.as_view()),
    path('city/ip', sxgeo_api.CityIp.as_view()),
    path('city/default', sxgeo_api.CityDefault.as_view()),
    path('widget_send', question_api.WidgetSend.as_view()),
]

