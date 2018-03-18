from apps.svem_system.views.api import ApiView
from apps.sxgeo.models import Cities, Country
from pysyge import GeoLocator
from django.conf import settings


class City(ApiView):
    @classmethod
    def get(cls, request):
        if not request.GET.get('keyword', False):
            return ''
        return Cities.city_like_as(
            request.GET['keyword'], [Country.RUSSIAN_ID, Country.UKRAINE_ID]
        )


class CityIp(ApiView):
    @classmethod
    def get(cls, request):
        geo_data = GeoLocator(settings.DATA_DIR + 'SxGeoCity.dat')
        ip = cls.get_client_ip(request)
        location = geo_data.get_location(ip, detailed=True)
        return {
            'id': location['info']['city']['id'],
            'name': location['info']['city']['name_ru']
        } if location else False


class CityDefault(ApiView):
    @classmethod
    def get(cls, request):
        return Cities.get_default([Country.RUSSIAN_ID, Country.UKRAINE_ID])
