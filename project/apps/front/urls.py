from django.conf.urls import url
from django.urls import path
from apps.front.views.front import Mainpage, LawyerPage, ReviewsPage

urlpatterns = [
    # Не менять порядок правил
    url(r'^$', Mainpage.as_view(), name='mainpage'),
    path('юрист/<int:id>/отзывы/', ReviewsPage.as_view(), name='lawyer_reviews'),
    path('юрист/<int:id>/', LawyerPage.as_view(), name='lawyer_page'),
    path('отзывы/', ReviewsPage.as_view(), name='reviews_page'),
]
