from django import forms
from django.forms import ModelForm, Select, inlineformset_factory
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from easy_select2 import select2_modelform, apply_select2

from apps.entry.models import Question, Answer, Files


def get_answer_form(question_id=0):
    """
    Форма редактирования/добавления ответа для ответов в вопросе
    :param question_id:
    :return:
    """
    class AnswerForm(ModelForm):
        parent = forms.ModelChoiceField(
            queryset=Answer.objects.filter(parent=None, on_question=question_id),
            required=False,
        )

        class Meta:
            model = Answer
            fields = ['author', 'content', 'parent']
            widgets = {
                'author': apply_select2(Select),
            }
    return AnswerForm

QuestionForm = select2_modelform(Question, attrs={'width': '100ex'})


class AnswersInLine(admin.StackedInline):
    model = Answer
    fk_name = 'on_question'
    show_change_link = True
    classes = ('collapse', 'collapse-closed')

    def get_formset(self, request, obj=None, **kwargs):
        question_id = 0 if obj is None else obj.pk
        return inlineformset_factory(
            parent_model=Question,
            model=self.model,
            form=get_answer_form(question_id),
            fk_name=self.fk_name, extra=0)


# Файлы, прикрепленные к вопросу
class FilesInLine(admin.StackedInline):
    model = Files
    fk_name = 'entry'
    extra = 0
    classes = ('collapse', 'collapse-closed')


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
    list_display = ('title', 'author', 'pub_date', 'like_count', 'reply_count')
    search_fields = ['title', 'content']
    list_filter = ('pub_date', 'status')
    inlines = (AnswersInLine, FilesInLine, )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'pub_date', 'like_count', 'reply_count', 'status')
    fields = ('content', ('author', 'status'), 'parent')
    inlines = (FilesInLine,)
