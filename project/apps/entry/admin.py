from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from easy_select2 import select2_modelform, select2_modelform_meta, apply_select2

from apps.entry.models import Question, Answer, Files, Offer

QuestionForm = select2_modelform(Question, attrs={'width': '100ex'},)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['author', 'content']
        widgets = {
            'author': apply_select2(forms.Select),
        }


class AnswersForQuestionInLine(admin.StackedInline):
    """
    Ответы первого уровня к вопросу
    """
    model = Answer
    form = AnswerForm
    fk_name = 'on_question'
    fields = ('author', 'content',)
    extra = 0
    show_change_link = True
    classes = ('collapse', 'collapse-closed')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent=None)


class AnswersForAnswerInLine(admin.StackedInline):
    model = Answer
    form = AnswerForm
    fk_name = 'parent'
    fields = ['author', 'content']
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


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Админка для модели Question.
    """
    form = QuestionForm
    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'content',)}),
        (_('Клиссификация'), {
            'fields': ('status', 'author', 'rubrics'),
            # 'classes': ('collapse', 'collapse-closed')
        }))
    radio_fields = {'status': admin.HORIZONTAL}
    list_display = ('title', 'author', 'pub_date', 'like_count', 'reply_count')
    search_fields = ['title', 'content']
    list_filter = ('pub_date', 'status')
    inlines = (AnswersForQuestionInLine, FilesInLine,)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    form = AnswerForm
    list_display = ('__str__', 'author', 'pub_date', 'like_count', 'reply_count', 'status')
    search_fields = ['content', ]
    readonly_fields = ('on_question',)
    fields = ('content', ('author', 'status'), 'on_question')
    radio_fields = {'status': admin.VERTICAL}
    inlines = (OfferInLine, AnswersForAnswerInLine, FilesInLine,)

    def get_queryset(self, request):
        """
        Только ответы первого уровня
        """
        qs = super().get_queryset(request)
        return qs.filter(parent=None)
