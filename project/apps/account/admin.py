from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import connection, models
from django.forms import CheckboxSelectMultiple
from image_cropping import ImageCroppingMixin

from apps.account.models import Info, Case, Education, Experience, Contact, Subscription
from apps.rubric.models import Rubric
from apps.sxgeo.models import Cities


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    search_fields = ['name_ru']
    list_display = ['full_name_ru']


class CityListFilter(SimpleListFilter):
    title = 'Город'
    parameter_name = 'city'

    def lookups(self, request, model_admin):
        cursor = connection.cursor()
        cursor.execute("""
          SELECT sc.id, CONCAT(name_ru, ' (', count(sc.id), ')')
          FROM mlo_auth_user AS mau
          LEFT JOIN sxgeo_cities AS sc ON (mau.city_id=sc.id)
          WHERE mau.role = 2
          GROUP BY sc.id
          ORDER BY count(sc.id) DESC, sc.name_ru
          """)

        return cursor.fetchall()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(city_id=self.value())
        else:
            queryset


@admin.register(Info)
class InfoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    model = Info
    list_display = ['user', ]
    list_per_page = 10
    fieldsets = (
        (None, {'fields': ('user', 'birth_date', 'sex', 'ym_purpose')}),
        ('Текст', {'fields': ('title', 'short', 'signature', 'about',)}),
        ('Фото', {'fields': ('orig', ('photo', 'pic'),)})
    )
    list_filter = (CityListFilter, )
    search_fields = ['user__last_name', 'user__id']
    raw_id_fields = ['user']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )
    autocomplete_fields = ['user']
    search_fields = ['user__last_name']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )
    autocomplete_fields = ['user']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )
    autocomplete_fields = ['user']
    search_fields = ['user__last_name']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )
    autocomplete_fields = ['user']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )
    autocomplete_fields = ['user', ]
    list_filter = (CityListFilter,)
    list_display = ['get_admin_title',]
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == 'question_rubrics':
            return Rubric.objects.filter(level=0)

        super().get_field_queryset(db, db_field, request)

