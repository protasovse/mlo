from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from apps.entry.models import Question, Answer, Files, Offer, ConsultState, Consult, ConsultStateLog, Likes, Review, \
    Entry


class AnswersForQuestionInLine(admin.StackedInline):
    """
    Ответы первого уровня к вопросу
    """
    model = Answer
    fk_name = 'on_question'
    fields = ('author', 'content',)
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


class ReviewInLine(admin.StackedInline):
    model = Review


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Админка для модели Question.
    """
    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'content',)}),
        (_('Клиссификация'), {
            'fields': ('status', 'author', 'rubrics', 'is_pay'),
            # 'classes': ('collapse', 'collapse-closed')
        }))
    autocomplete_fields = ['rubrics', 'author']
    radio_fields = {'status': admin.HORIZONTAL}
    list_display = ('title', 'author', 'pub_date', 'like_count', 'reply_count')
    search_fields = ['id', 'title', 'content', 'author__last_name', 'author__email']
    list_filter = ('pub_date', 'status')
    inlines = (AnswersForQuestionInLine, FilesInLine,)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'pub_date', 'like_count', 'reply_count', 'status')
    search_fields = ['content', 'author__last_name', 'author__email']
    # readonly_fields = ('on_question',)
    fields = ('content', ('author', 'status'), 'on_question')
    autocomplete_fields = ['author', 'on_question']
    radio_fields = {'status': admin.VERTICAL}
    inlines = (OfferInLine, AnswersForAnswerInLine, FilesInLine,)

    def get_queryset(self, request):
        """
        Только ответы первого уровня
        """
        qs = super().get_queryset(request)
        return qs.filter(parent=None)


@admin.register(Consult)
class ConsultAdmin(admin.ModelAdmin):
    """
    Админка для модели Consult.
    """
    list_display = ('question_id', 'pk', 'cost', 'expert_id', 'state',)
    fieldsets = (
        (_('Content'), {
            'fields': ('question', 'cost', 'expert', 'state')}),
        )
    autocomplete_fields = ['expert']
    raw_id_fields = ['question']
    list_filter = ['state']
    # inlines = (AnswersForQuestionInLine, FilesInLine,)


@admin.register(ConsultState)
class ConsultStateAdmin(admin.ModelAdmin):
    pass


@admin.register(ConsultStateLog)
class ConsultStateLogAdmin(admin.ModelAdmin):
    list_display = ('consult', 'date', 'consult_state',)
    list_filter = ('consult_state',)


class LikeWithReviewFilter(SimpleListFilter):
    title = 'Отзывы'
    parameter_name = 'with_review'

    def lookups(self, request, model_admin):
        return (
            ('true', _('С текстом отзыва')),
            ('false', _('Без текста отзыва'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.exclude(review__review=None)
        else:
            queryset


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('date', 'entry_id', 'value', 'user', 'review', 'title_for_admin')
    search_fields = ['entry__pk', 'user__last_name']
    raw_id_fields = ['user', 'entry', ]
    inlines = (ReviewInLine,)
    list_filter = (LikeWithReviewFilter,)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    raw_id_fields = ['author', ]
