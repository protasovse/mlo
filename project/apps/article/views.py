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

        similar_articles = Article.published.filter(pk__lt=article.pk, dir=article.dir).order_by('-pk')[:10]

        context.update({
            'article': article,
            'similar_articles': similar_articles,
        })

        return context
