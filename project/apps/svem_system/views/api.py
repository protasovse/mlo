from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import connection
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from apps.svem_system.exceptions import ApiPublicException, ApiException


class ApiView(View):

    user = False
    debug = False
    """
    mixin for API view
    get_data_for_response - method that return data for view
    get - method returns data in specific format
    """
    def options(self, request, *args, **kwargs):
        response = super(ApiView, self).options(request, *args, **kwargs)
        del response['Content-Type']
        response.status_code = 204
        response['Access-Control-Allow-Methods'] = response['Allow']
        return response

    @classmethod
    def is_debug_mode(cls, request):
        return settings.DEBUG

    def response(self, kwargs):
        raise ApiException('method "get_data_for_response" is not declare')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        request_status = 500
        handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        if request.method.lower() == 'options':
            return handler(request, *args, **kwargs)
        try:
            with transaction.atomic():
                result = super(ApiView, self).dispatch(request, *args, **kwargs)
                response = {
                    'success': True,
                }
                if type(result) == bool:
                    print(result)
                    response = {'success': result}
                elif result is not None:
                    response['data'] = result
                request_status = 200
        except ApiPublicException as e:
            response = {
                'success': False,
                'error': str(e),
                'code': e.code
            }
            request_status = e.request_status
        except ValidationError as e:
            response = {
                'success': False,
                'error': e.messages[0]
            }
            if self.is_debug_mode(request):
                response['exception'] = type(e).__name__
                response['error'] = str(e)
        except Exception as e:
            response = {
                'success': False,
                'error': 'системная ошибка'
            }
            if self.is_debug_mode(request):
                response['exception'] = type(e).__name__
                response['error'] = str(e)
        if self.is_debug_mode(request):
            response['queries'] = connection.queries
        return JsonResponse(response, status=request_status)

