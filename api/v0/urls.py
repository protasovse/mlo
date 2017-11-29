from django.conf.urls import url, include
from rest_framework import routers

from base.mlo_auth.api import views as mlo_auth_view_api
# from entry import view_api as entry_view_api
from entry.rubric import view_api as rubric_view_api

# router = routers.DefaultRouter()

# router.register(r'users', mlo_auth_view_api.UserViewSet, base_name='user')
# router.register(r'lawyers', mlo_auth_view_api.LawyerViewSet, base_name='lawyer')
# router.register(r'clients', mlo_auth_view_api.ClientViewSet, base_name='client')

# router.register(r'questions', entry_view_api.QuestionViewSet)

urlpatterns = [
#    url(r'^', include(router.urls)),
    url(r'^rubrics/$', rubric_view_api.RubricList.as_view(), name='rubric-list'),
    url(r'^rubrics/(?P<pk>[0-9]+)/$', rubric_view_api.RubricDetail.as_view(), name='rubric-detail'),
    url(r'^rubrics/child/(?P<pk>[0-9]+)/$', rubric_view_api.RubricChildrenOfList.as_view(), name='rubric-child-list'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
