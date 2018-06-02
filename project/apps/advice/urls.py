from django.urls import path

from apps.advice.views.front import advice_to_payment_confirmed, advice_check_of_overdue

urlpatterns = [
    path('to_payment_confirmed/', advice_to_payment_confirmed, name='payment_confirmed'),
    path('check_of_overdue/', advice_check_of_overdue, name='payment_confirmed'),
]
