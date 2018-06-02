from django.urls import path, include

from apps.account.views import InfoEdit, UserEdit, ContactEdit, EducationEdit, ExperienceEdit, AdviceSchedulerEdit, \
    SubscriptionEdit

app_name = 'account'

urlpatterns = [
    path(
        'вопросы/',
        include('apps.entry.urls.personal_questions', namespace='personal_questions')
    ),

    path(
        'редактировать-профиль/',
        InfoEdit.as_view(template_name='account/edit/additional.html'),
        name='edit_profile'
    ),

    path(
        'регистрационные-данные/',
        UserEdit.as_view(template_name='account/edit/main.html'),
        name='edit_user_data'
    ),

    path(
        'образование/',
        EducationEdit.as_view(template_name='account/edit/education.html'),
        name='edit_education'
    ),

    path(
        'опыт-работы/',
        ExperienceEdit.as_view(template_name='account/edit/experience.html'),
        name='edit_experience'
    ),

    path(
        'контакты/',
        ContactEdit.as_view(template_name='account/edit/contact.html'),
        name='edit_contact'
    ),

    path(
        'платные-заявки/',
        AdviceSchedulerEdit.as_view(template_name='account/edit/scheduler.html'),
        name='edit_scheduler'
    ),

    path(
        'уведомления/',
        SubscriptionEdit.as_view(template_name='account/edit/subscription.html'),
        name='edit_subscription'
    ),
]
