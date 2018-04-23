from django.urls import path

from apps.account.views import InfoEdit, UserEdit, ContactEdit, EducationEdit, ExperienceEdit

app_name = 'account'

urlpatterns = [
    # path('редактировать-профиль/', account.views.main, name='edit'),
    path('редактировать-профиль/', InfoEdit.as_view(template_name='account/edit/additional.html'), name='edit'),
    path('регистрационные-данные/', UserEdit.as_view(template_name='account/edit/main.html'), name='edit_regdata'),
    path('образование/', EducationEdit.as_view(template_name='account/edit/education.html'), name='edit_education'),
    path('опыт-работы/', ExperienceEdit.as_view(template_name='account/edit/experience.html'), name='edit_experience'),
    path('контакты/', ContactEdit.as_view(template_name='account/edit/contact.html'), name='edit_contact'),
]
