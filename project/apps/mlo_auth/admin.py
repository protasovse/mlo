from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.forms import modelform_factory
from django.utils.translation import ugettext_lazy as _

from apps.account.models import Case, Education, Experience
from apps.mlo_auth.models import User


class CaseInLine(admin.StackedInline):
    model = Case
    extra = 0
    classes = ('collapse', 'collapse-closed')


class EducationInLine(admin.StackedInline):
    model = Education
    extra = 0
    classes = ('collapse', 'collapse-closed')


class ExperienceInLine(admin.StackedInline):
    model = Experience
    extra = 0
    classes = ('collapse', 'collapse-closed')


class MloUserAdmin(UserAdmin):

    add_form = UserCreationForm

    list_display = ('get_full_name', 'email', 'is_staff',)

    list_filter = ('is_active', 'role')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_joined')}),
        (_('Personal info'), {'fields': ('first_name', 'patronymic', 'last_name', 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'is_staff')}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'role', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'patronymic', 'last_name', 'id')
    ordering = ('id',)
    filter_horizontal = ()

    inlines = (CaseInLine, EducationInLine, ExperienceInLine)


admin.site.register(User, MloUserAdmin)
admin.site.unregister(Group)
