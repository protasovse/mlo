from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.advice.models import Advice, StatusLog, Queue, Scheduler, Expert


@admin.register(Advice)
class AdviceAdmin(admin.ModelAdmin):
    """
    Админка для модели Consult.
    """
    list_display = ('question_id', 'pk', 'cost', 'expert', 'status', 'payment_date',)
    fieldsets = (
        (_('Content'), {
            'fields': ('question', 'cost', 'expert', 'status', 'payment_date',)}),
        )
    autocomplete_fields = ['expert']
    raw_id_fields = ['question']
    list_filter = ['status']
    # inlines = (AnswersForQuestionInLine, FilesInLine,)


@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('advice', 'date', 'status',)
    list_filter = ('status',)


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('expert', 'order', 'is_active',)
    autocomplete_fields = ['expert', ]


@admin.register(Scheduler)
class SchedulerAdmin(admin.ModelAdmin):
    # list_display = ('user', 'timezone',)
    autocomplete_fields = ['expert', ]


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user', ]
