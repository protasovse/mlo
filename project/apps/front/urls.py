from django.conf.urls import url
from django.urls import path, include
from apps.front.views.front import Mainpage, LawyerPage, ReviewsPage, TermsOfUse, About

urlpatterns = [
    # Не менять порядок правил
    url(r'^$', Mainpage.as_view(), name='mainpage'),
    path('юрист/<int:id>/отзывы/', ReviewsPage.as_view(), name='lawyer_reviews'),
    path('юрист/<int:id>/', LawyerPage.as_view(), name='lawyer_page'),
    path('отзывы/', ReviewsPage.as_view(), name='reviews_page'),
    path('пользовательское-соглашение/', TermsOfUse.as_view(), name='terms_of_use'),
    path('о-проекте/', About.as_view(), name='about'),


    # Все остальные гкд проверяем на редирект
    url(r'^', include('apps.front.urls_redirect_from_svem')),
]
