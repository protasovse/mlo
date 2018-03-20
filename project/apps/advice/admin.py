from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.advice.models import Advice, StatusLog


@admin.register(Advice)
class ConsultAdmin(admin.ModelAdmin):
    """
    Админка для модели Consult.
    """
    list_display = ('question_id', 'pk', 'cost', 'expert', 'status',)
    fieldsets = (
        (_('Content'), {
            'fields': ('question', 'cost', 'expert', 'status')}),
        )
    autocomplete_fields = ['expert']
    raw_id_fields = ['question']
    list_filter = ['status']
    # inlines = (AnswersForQuestionInLine, FilesInLine,)


@admin.register(StatusLog)
class ConsultStateLogAdmin(admin.ModelAdmin):
    list_display = ('advice', 'date', 'status',)
    list_filter = ('status',)

