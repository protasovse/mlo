from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^вопросы/', include('apps.entry.urls_questions', namespace='questions')),

    url(r'^api/v0/entries/', include('apps.entry.api.urls', namespace='entries-api')),
    url(r'^api/v0/users/', include('apps.mlo_auth.api.urls', namespace="users-api")),
    url(r'^api/v0/auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Api
    # url(r'^api/v0/', include(api.v0.urls, namespace='api')),

    url(r'^рубрики/', include('apps.rubric.urls', namespace='rubrics')),

    # url(r'^', include('apps.rubric.urls', namespace='rubrics')),

    path('auth/', include('apps.svem_auth.urls')),
    path('api/', include('config.api_urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
