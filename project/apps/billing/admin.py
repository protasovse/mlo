from django.contrib import admin

from apps.billing.models import Purse


@admin.register(Purse)
class PurseAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']
    autocomplete_fields = ['user']
