from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^вопросы/', include('entry.urls_questions', namespace='questions')),

    url(r'^api/v0/entries/', include('entry.api.urls', namespace='entries-api')),
    url(r'^api/v0/users/', include('base.mlo_auth.api.urls', namespace="users-api")),
    url(r'^api/v0/auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Api
    # url(r'^api/v0/', include(api.v0.urls, namespace='api')),

    url(r'^рубрики/', include('entry.rubric.urls', namespace='rubrics')),
    url(r'^', include('entry.rubric.urls', namespace='rubrics')),
]
