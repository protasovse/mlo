from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
# from django.contrib.sitemaps import views as sitemap_views
from django.urls import path, re_path
from django.contrib import admin, sitemaps
# from django.views.decorators.cache import cache_page

from apps.mlo_auth.admin import LoginView
from apps.question.views.front import AskQuestion

urlpatterns = [

    # url(r'^sitemap/', include('apps.sitemap.urls', namespace='sitemap')),
    # path('sitemap.xml', cache_page(86400)(sitemap_views.index), {'sitemaps': sitemaps}),

    path('задать-вопрос/', AskQuestion.as_view(), name='ask_question'),
    path('вопрос/', include('apps.question.urls', namespace='question')),
    path('вопросы/', include('apps.entry.urls.questions', namespace='questions')),
    path('личный-кабинет/', include('apps.account.urls', namespace='personal')),

    path('admin/login/', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('advice/', include('apps.advice.urls')),
    path('auth/', include('apps.svem_auth.urls')),
    path('api/', include('config.api_urls')),
    path('select2/', include('django_select2.urls')),

    # Остальные url обрабатываем в приложении front
    url(r'^', include('apps.front.urls', namespace='front')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns