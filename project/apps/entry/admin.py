from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.advice.models import Advice
from apps.entry.models import Question, Answer, Files, Offer, Entry


class AnswersForQuestionInLine(admin.StackedInline):
    """
    Ответы первого уровня к вопросу
    """
    model = Answer
    fk_name = 'on_question'
    fields = ('author', 'content')
    autocomplete_fields = ['author']
    extra = 0
    show_change_link = True
    classes = ('collapse', 'collapse-closed')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent=None)


class AnswersForAnswerInLine(admin.StackedInline):
    model = Answer
    fk_name = 'parent'
    fields = ['author', 'content']
    autocomplete_fields = ['author']
    extra = 0
    show_change_link = True
    classes = ('collapse', 'collapse-closed')


class FilesInLine(admin.StackedInline):
    # Файлы
    model = Files
    fk_name = 'entry'
    extra = 0
    classes = ('collapse', 'collapse-closed')


class OfferInLine(admin.StackedInline):
    # Предложения платных услуг
    model = Offer
    fk_name = 'answer'
    readonly_fields = ['status']
    fields = [('cost', 'status')]
    extra = 1
    # classes = ('collapse', 'collapse-closed')


class AdviceInLine(admin.StackedInline):
    model = Advice
    fk_name = 'question'
    autocomplete_fields = ['expert']
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Админка для модели Question.
    """
    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'content',)}),
        (_('Клиссификация'), {
            'fields': ('status', 'author', 'rubric', 'is_pay', 'reply_count', )}),
        (_('Дополнительные поля'), {
            'fields': ('city', 'phone', 'first_name')}),
    )
    autocomplete_fields = ['rubric', 'author', 'city']
    radio_fields = {'status': admin.HORIZONTAL}
    list_display = ('title', 'author', 'pub_date', 'like_count', 'reply_count', 'status', 'is_pay')
    search_fields = ['id', 'title', 'content', 'author__last_name', 'author__email']
    list_filter = ('pub_date', 'status', 'is_pay')
    inlines = (AnswersForQuestionInLine, FilesInLine, AdviceInLine)
    list_per_page = 10


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content', 'on_question_id', 'author', 'pub_date', 'like_count', 'reply_count', 'status')
    search_fields = ['content']
    # readonly_fields = ('on_question',)
    ordering = ['-thread']
    fields = ('content', ('author', 'status'), 'on_question')
    autocomplete_fields = ['author', 'on_question']
    radio_fields = {'status': admin.VERTICAL}
    inlines = (OfferInLine, AnswersForAnswerInLine, FilesInLine,)
    list_per_page = 10

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term.isdigit():
            queryset = Answer.objects.filter(pk=search_term)
        return queryset, False

    def get_queryset(self, request):
        """
        Только ответы первого уровня
        """
        qs = super().get_queryset(request)
        return qs.filter(parent=None)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    raw_id_fields = ['author', ]
