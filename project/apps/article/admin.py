from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from apps.article.models import Article, Dir


@admin.register(Dir)
class DirAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'slug')
    list_display = ('name', 'slug')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Админка для модели Article.
    """
    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'content', 'dir')}),
        (_('Клиссификация'), {
            'fields': ('status', 'author', 'rubric', 'reply_count', )}),
    )
    autocomplete_fields = ['rubric', 'author']
    radio_fields = {'status': admin.HORIZONTAL}
    list_display = ('entry_ptr_id', 'title', 'author', 'pub_date', 'like_count', 'reply_count', 'status',)
    search_fields = ['id', 'title', 'content', 'author__last_name', 'author__email']
    list_filter = ('pub_date', 'status', 'dir')
    list_per_page = 20
