from apps.svem_system.views.api import ApiView
from apps.entry.models import Question
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
        """
        create a question
        :param request:
        :return:
        """
        params = self.get_put(request)
        q = Question(
            title=params['title'],
            content=params['content'],
        )
        return 'file uploaded'

