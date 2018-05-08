from django.conf.urls import url
from django.urls import path, include
from apps.front.views.front import Mainpage, LawyerPage, ReviewsPage, TermsOfUse, About, LawyersListPage

urlpatterns = [
    # Не менять порядок правил
    url(r'^$', Mainpage.as_view(), name='mainpage'),

    path('юристы/', LawyersListPage.as_view(), name='lawyers_list_page'),
    path('юристы/<int:page>/', LawyersListPage.as_view(), name='lawyers_list_page'),
    path('юристы/город/<city>-<int:city_id>/', LawyersListPage.as_view(), name='lawyers_list_page'),
    path('юристы/город/<city>-<int:city_id>/<int:page>/', LawyersListPage.as_view(), name='lawyers_list_page'),

    path('юрист/<int:id>/отзывы/', ReviewsPage.as_view(), name='lawyer_reviews'),
    path('юрист/<int:id>/отзывы/<int:page>/', ReviewsPage.as_view(), name='lawyer_reviews'),

    path('юрист/<int:id>/', LawyerPage.as_view(), name='lawyer_page'),

    path('отзывы/', ReviewsPage.as_view(), name='reviews_page'),
    path('отзывы/<int:page>/', ReviewsPage.as_view(), name='reviews_page'),

    path('пользовательское-соглашение/', TermsOfUse.as_view(), name='terms_of_use'),
    path('о-проекте/', About.as_view(), name='about'),

    # Все остальные url проверяем на редирект
    url(r'^', include('apps.front.urls_redirect_from_svem')),
]
