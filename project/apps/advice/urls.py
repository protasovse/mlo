from django.urls import path

from apps.advice.views import advice_to_payment_confirmed

urlpatterns = [
    path('to_payment_confirmed', advice_to_payment_confirmed, name='list'),
]
