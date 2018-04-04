import pymorphy2
from django.utils.deprecation import MiddlewareMixin
from pysyge import GeoLocator

from config import settings


class LocationIdentify(MiddlewareMixin):
    def process_request(self, request):
        geo_data = GeoLocator(settings.DATA_DIR + 'SxGeoCity.dat')
        ip = self.get_client_ip(request)
        location = geo_data.get_location(ip, detailed=True)
        if not location:
            location = geo_data.get_location('195.239.1.253', detailed=True)

        city_name = location['info']['city']['name_ru']
        city_id = location['info']['city']['id']
        region_name = location['info']['region']['name_ru']
        region_id = location['info']['region']['id']

        morph = pymorphy2.MorphAnalyzer()
        c = morph.parse(city_name)[0]

        request.user.location = {
            'city_id': city_id,
            'city_name': city_name,
            'city_name_loc': c.inflect({'loc2'}).word.title(),
            'region_id': region_id,
            'region_name': region_name,
        }

        request.user.hot_line_phone = settings.HOT_LINE_PHONES[region_name] \
            if region_name in settings.HOT_LINE_PHONES \
            else settings.HOT_LINE_PHONES['остальные']

    @classmethod
    def get_client_ip(cls, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
