from apps.svem_system.views.api import ApiView
from apps.sxgeo.models import Cities


class City(ApiView):
    @classmethod
    def get(cls, request):
        if not request.GET.get('keyword', False):
            return ''
        return Cities.city_like_as(request.GET['keyword'])
