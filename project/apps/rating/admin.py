from django.contrib import admin

from apps.rating.models import Type, RatingScore, Rating


@admin.register(Type)
class TypesAdmin(admin.ModelAdmin):
    pass


@admin.register(RatingScore)
class RatingScoreAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'day_rate', 'week_rate', 'month_rate', 'rate', ]
    autocomplete_fields = ['user']

