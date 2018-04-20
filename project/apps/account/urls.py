from django.urls import path

from apps.account.views import InfoEdit, UserEdit

app_name = 'account'

urlpatterns = [
    # path('редактировать-профиль/', account.views.main, name='edit'),
    path('редактировать-профиль/', InfoEdit.as_view(template_name='account/edit/additional.html'), name='edit'),
    path('регистрационные-данные/', UserEdit.as_view(template_name='account/edit/main.html'), name='edit_regdata'),
    path('образование/', InfoEdit.as_view(template_name='account/edit/education.html'), name='edit_education'),
    path('опыт-работы/', InfoEdit.as_view(template_name='account/edit/experience.html'), name='edit_experience'),
    path('контакты/', InfoEdit.as_view(template_name='account/edit/contact.html'), name='edit_contact'),
]
