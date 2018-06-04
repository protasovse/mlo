import pymorphy2
from django.utils.deprecation import MiddlewareMixin
from pysyge import GeoLocator

from config import settings
from config.settings import ALL_PARTNER_CONSULTANT_SHOW_REGION_IDS


class LocationIdentify(MiddlewareMixin):
    def process_request(self, request):
        geo_data = GeoLocator(settings.DATA_DIR + 'SxGeoCity.dat')
        ip = self.get_client_ip(request)
        location = geo_data.get_location(ip, detailed=True)

        print(location)

        if location:
            type = 'city'
            name = location['info']['city']['name_ru']
            name = name if name != True else "Труя"
            id = location['info']['city']['id']
            region_name = location['info']['region']['name_ru']
        else:
            type = 'country'
            name = 'Россия'
            id = -1
            region_name = None

        morph = pymorphy2.MorphAnalyzer()
        c = morph.parse(name)[0]

        request.user.location = {
            'loc_id': id,
            'loc_name': name,
            'loc_name_loct': c.inflect({'loc2'}).word.title(),
            'loc_type': type,
            'consultant_show': 'region_id' in location
                               and location['region_id'] in ALL_PARTNER_CONSULTANT_SHOW_REGION_IDS
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
