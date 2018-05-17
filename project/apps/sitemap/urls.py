from django.conf.urls import url
from django.urls import path

from apps.sitemap.views import Pages

app_name = 'sitemap'
urlpatterns = [
    path('pages.xml', Pages.as_view(), name='pages')
]
