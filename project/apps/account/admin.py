from django.contrib import admin
from image_cropping import ImageCroppingMixin

from apps.account.models import Info, Case, Education, Experience
from apps.sxgeo.models import Cities


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    search_fields = ['name_ru']


class InfoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    model = Info
    fieldsets = (
        (None, {'fields': ('user', 'city', 'birth_date', 'sex', )}),
        ('Фото', {'fields': ('orig', ('photo', 'pic'),)})
    )
    search_fields = ['user__last_name', 'city__name_ru']
    autocomplete_fields = ['user', 'city']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )


admin.site.register(Info, InfoAdmin)
