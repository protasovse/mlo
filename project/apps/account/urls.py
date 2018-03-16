from django.urls import path

from apps.account.views import AccountDetail

app_name = 'account'

urlpatterns = [
    path('редактировать-профиль/', AccountDetail.as_view(template_name='account/edit/main.html'), name='edit'),
    path('о-себе/', AccountDetail.as_view(template_name='account/edit/about.html'), name='edit_about'),
    path('образование/', AccountDetail.as_view(template_name='account/edit/education.html'), name='edit_education'),
    path('опыт-работы/', AccountDetail.as_view(template_name='account/edit/experience.html'), name='edit_experience'),
    path('контакты/', AccountDetail.as_view(template_name='account/edit/contact.html'), name='edit_contact'),
]
