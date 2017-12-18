from django.contrib import admin
from image_cropping import ImageCroppingMixin

from apps.account.models import Info, Case, Education, Experience


class InfoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    model = Info
    fieldsets = (
        (None, {'fields': ('user', 'birth_date', 'sex', )}),
        ('Фото', {'fields': ('orig', ('photo', 'pic'),)})
    )


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
