from django.contrib import admin
from image_cropping import ImageCroppingMixin

from apps.front.models import CityMeta


@admin.register(CityMeta)
class InfoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ['city', ]
    list_per_page = 10
    fieldsets = (
        (None, {'fields': ('city', 'lawyers_page_description')}),
        ('Обложка', {'fields': ('lawyers_page_cover_orig', 'lawyers_page_cover',)})
    )

    autocomplete_fields = ('city',)

