from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.translation import ugettext_lazy as _

from mptt.forms import TreeNodeChoiceField
from django_mptt_admin.admin import DjangoMpttAdmin

from entry.rubric.models import Rubric


class RubricAdminForm(forms.ModelForm):
    """
    Форма для адмики рубрик.
    """
    parent = TreeNodeChoiceField(
        label=_('Родительская рубрика'),
        empty_label=_('Нет родительской рубрики'),
        level_indicator='……', required=False,
        queryset=Rubric.objects.all())

    def __init__(self, *args, **kwargs):
        super(RubricAdminForm, self).__init__(*args, **kwargs)
        self.fields['parent'].widget = RelatedFieldWidgetWrapper(
            self.fields['parent'].widget,
            Rubric.parent.field.remote_field,
            self.admin_site)

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


@admin.register(Rubric)
class RubricAdmin(DjangoMpttAdmin):
    fields = ('name', 'description', 'slug', 'parent')
    list_display = ('title_for_admin', 'slug')
    search_fields = ('name',)
    raw_id_fields = ('parent',)
    list_filter = ('tree_id',)
    # inlines = (RubricsInLine, )
    use_context_menu=True
    item_label_field_name = 'title_for_admin'
