from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import path, re_path
from django.contrib import admin
from apps.mlo_auth.admin import LoginView


urlpatterns = [

    path('admin/login/', LoginView.as_view(), name='login'),
    url(r'^admin/', admin.site.urls),

    re_path('^задать-вопрос/', include('apps.question.urls')),

    url(r'^вопрос/', include('apps.entry.urls.question', namespace='question')),
    url(r'^вопросы/', include('apps.entry.urls.questions', namespace='questions')),
    url(r'^личный-кабинет/вопросы/', include('apps.entry.urls.personal_questions', namespace='personal_questions')),
    url(r'^личный-кабинет/', include('apps.account.urls', namespace='personal')),

    path('auth/', include('apps.svem_auth.urls')),
    path('api/', include('config.api_urls')),

    url(r'^select2/', include('django_select2.urls')),

    url(r'^', include('apps.front.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns