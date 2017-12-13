from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.entry.models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Админка для модели Question.
    """
    fieldsets = (
        (_('Content'), {
            'fields': (('title', 'status'), 'content',)}),
        (_('Клиссификация'), {
            'fields': ('author', 'rubrics'),
            'classes': ('collapse', 'collapse-closed')
        }))
    list_display = ('title', 'author', 'pub_date', 'like_count', 'reply_count')
    raw_id_fields = ('author',)
    search_fields = ['title', 'content']
    list_filter = ('pub_date', 'status')
    # inlines = (FilesInLine, AnswersInLine, CommentsInLine)

admin.site.register(Answer)
