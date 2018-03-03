from django.contrib import admin
from image_cropping import ImageCroppingMixin

from apps.account.models import Info, Case, Education, Experience, Contact, RatingTypes, Rating, RatingResult
from apps.sxgeo.models import Cities


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    search_fields = ['name_ru']
    list_display = ['full_name_ru']


class InfoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    model = Info
    fieldsets = (
        (None, {'fields': ('user', 'city', 'birth_date', 'sex', )}),
        ('Текст', {'fields': ('status', 'signature', 'about', )}),
        ('Фото', {'fields': ('orig', ('photo', 'pic'),)})
    )
    search_fields = ['user__last_name']
    autocomplete_fields = ['city']
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


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )
    autocomplete_fields = ['user']


@admin.register(RatingTypes)
class RatingTypesAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(RatingResult)
class RatingResultAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']


admin.site.register(Info, InfoAdmin)
