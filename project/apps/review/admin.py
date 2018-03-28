from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

from apps.review.models import Likes, Review


class ReviewInLine(admin.StackedInline):
    model = Review


class LikeWithReviewFilter(SimpleListFilter):
    title = 'Отзывы'
    parameter_name = 'with_review'

    def lookups(self, request, model_admin):
        return (
            ('true', _('С текстом отзыва')),
            ('false', _('Без текста отзыва'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.exclude(review__review=None)
        else:
            return queryset


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ['date', 'entry', 'value', 'user', 'review', ]
    search_fields = ['entry__pk', 'user__last_name', 'review__review', ]
    raw_id_fields = ['user', 'entry', ]
    inlines = (ReviewInLine,)
    list_filter = (LikeWithReviewFilter,)
    ordering = ('-date', )
    list_per_page = 15



