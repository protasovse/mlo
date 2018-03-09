from apps.svem_system.views.api import ApiView
from django.http import QueryDict


class Question(ApiView):
    def get(self, request):
        return 'get question'

    def post(self, request):
        post, files = request.parse_file_upload(request.META, request)
        with open(files['file'].name, 'wb+') as destination:
            for chunk in files['file'].chunks():
                destination.write(chunk)
        return 'file {} uploaded'.format(files['file'].name)

    def put(self, request):
        if request.content_type.startswith('multipart'):
            put, files = request.parse_file_upload(request.META, request)
            request.FILES.update(files)
            request.PUT = put.dict()
        else:
            request.PUT = QueryDict(request.body)

        print(request.PUT)

        return 'file uploaded'

