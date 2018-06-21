from django.conf.urls import url
from django.urls import path

from apps.article.views import ArticleDetail

app_name = 'article'
urlpatterns = [
    path('<str:slug>/<int:id>/', ArticleDetail.as_view(), name='article')
]
