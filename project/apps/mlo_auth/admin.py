from django.contrib import admin
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django import forms
from apps.account.models import Case, Education, Experience, Contact
from apps.advice.models import Scheduler
from apps.mlo_auth.models import User
from django.contrib.auth.forms import AuthenticationForm as AdminAuthenticationForm
from django.contrib.auth.views import LoginView as AdminLoginView

UserModel = get_user_model()


class ContactInLine(admin.StackedInline):
    model = Contact
    extra = 0
    classes = ('collapse', 'collapse-closed')


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


def make_expert(modeladmin, request, queryset):
    queryset.update(is_expert=True)
    from apps.advice.utils import queue_add_user
    for exp in queryset.all():
        Scheduler.objects.get_or_create(expert_id=exp.pk)
        queue_add_user(exp.pk)


make_expert.short_description = "Сделать пользователя экспертом"


def make_non_expert(modeladmin, request, queryset):
    queryset.update(is_expert=False)
    from apps.advice.utils import queue_del_user
    for exp in queryset.all():
        queue_del_user(exp.pk)


make_non_expert.short_description = "Убрать пользователя из экспертов"


class MloUserAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display = ('id', 'get_full_name', 'email', 'is_active', 'role', 'is_expert', 'date_joined')

    list_filter = ('is_active', 'role', 'is_expert')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone', 'city',)}),
        (_('Personal info'), {'fields': ('first_name', 'patronymic', 'last_name', 'role',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'is_staff', 'is_expert')}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'role', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name',)

    autocomplete_fields = ('city',)
    ordering = ('id',)
    list_per_page = 15
    filter_horizontal = ()
    inlines = (ContactInLine, CaseInLine, EducationInLine, ExperienceInLine)

    actions = [make_expert, make_non_expert]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term.isdigit():
            queryset = get_user_model().objects.filter(pk=search_term)

        return queryset, False


class AuthenticationForm(AdminAuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            self.user_cache = authenticate(email=username, password=password)
            if self.user_cache is None:
                # An authentication backend may reject inactive users. Check
                # if the user exists and is inactive, and raise the 'inactive'
                # error if so.
                try:
                    self.user_cache = UserModel._default_manager.get_by_natural_key(username)
                except UserModel.DoesNotExist:
                    pass
                else:
                    self.confirm_login_allowed(self.user_cache)
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class LoginView(AdminLoginView):
    template_name = 'admin/login.html'

    def get_form_class(self):
        return AuthenticationForm


admin.site.register(User, MloUserAdmin)
admin.site.unregister(Group)
