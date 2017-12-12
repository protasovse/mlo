from rest_framework import routers

from django.conf.urls import url, include

from base.mlo_auth.api import views as mlo_auth_view_api

router = routers.DefaultRouter()
router.register(r'', mlo_auth_view_api.UserViewSet)

app_name = 'auth_api'
urlpatterns = [
    url(r'^', include(router.urls)),
]
