from django.http import Http404
from django.views.generic import TemplateView

from apps.article.models import Article


class ArticleDetail(TemplateView):
    template_name = 'article/article_detail.html'

    def get_context_data(self, slug, id, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            article = Article.objects.select_related().get(pk=id, dir__slug=slug)
        except Article.DoesNotExist:
            raise Http404("Article doesn't exists")

        context.update({
            'article': article
        })

        return context
