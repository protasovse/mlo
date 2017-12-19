from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.translation import ugettext_lazy as _
from django_mptt_admin.admin import DjangoMpttAdmin
from easy_select2 import Select2
from mptt.forms import TreeNodeChoiceField

from apps.rubric.models import Rubric


class RubricAdminForm(forms.ModelForm):
    """
    Форма для адмики рубрик.
    """
    parent = TreeNodeChoiceField(
        label=_('Родительская рубрика'),
        empty_label=_('Нет родительской рубрики'),
        level_indicator='• • ', required=False,
        queryset=Rubric.objects.all(),
        widget=Select2({'width': '100ex'}),
    )

    # def __init__(self, *args, **kwargs):
    #     super(RubricAdminForm, self).__init__(*args, **kwargs)
    #     self.fields['parent'].widget = RelatedFieldWidgetWrapper(
    #         self.fields['parent'].widget,
    #         Rubric.parent.field.remote_field,
    #         self.admin_site)

    def clean_parent(self):
        """
        Проверим не является ли родительская категория самой.
        """
        data = self.cleaned_data['parent']
        if data == self.instance:
            raise forms.ValidationError(
                _('A category cannot be parent of itself.'),
                code='self_parenting')
        return data

    class Meta:
        model = Rubric
        fields = forms.ALL_FIELDS


class TreeIdFilter(admin.SimpleListFilter):
    """
    Фильтр в правой колонке
    """
    title = _('Рубрики')
    parameter_name = 'parent_id'

    def lookups(self, request, model_admin):
        if self.value() is None:
            rubrics = Rubric.objects.filter(parent=None)
        else:
            rq = Rubric.objects.get(pk=self.value())
            rubrics = rq.get_children()
            if rubrics.count() == 0:
                rubrics = rq.get_siblings(include_self=True)

        l = ()
        for r in rubrics:
            l = l+((
                       r.pk,
                       "%s (%d)" % (r.name, r.get_descendants().count())
                   ),)

        return l

    def queryset(self, request, queryset):
        # print(self.value())
        if self.value() is None:
            return Rubric.objects.all()
        rq = Rubric.objects.get(pk=self.value())
        return Rubric.objects.get(pk=self.value()).get_descendants(include_self=True)


@admin.register(Rubric)
class RubricAdmin(DjangoMpttAdmin, admin.ModelAdmin):
    form = RubricAdminForm
    fieldsets = (
        (None, {
            'fields': ('name', 'parent',)}),
        (_('Описание'), {
            'fields': ('description', 'slug'),
            'classes': ('collapse', 'collapse-closed')
        }))
    list_display = ('title_for_admin', 'slug')
    search_fields = ('name',)
    list_filter = (TreeIdFilter,)
    use_context_menu = True
    item_label_field_name = 'title_for_admin'
