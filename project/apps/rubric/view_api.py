from apps.svem_system.views.api import ApiView
from apps.rubric.models import Rubric


class Rubrics(ApiView):
    def get(self, request):
        filters = {}
        if 'keyword' in request.GET.keys():
            filters['name__icontains'] = request.GET.get('keyword')
        if 'level' in request.GET.keys():
            filters['level'] = request.GET.get('level')

        return [
            {
                'id': x['id'],
                'name': x['name'],
                'slug': x['slug']
            }
            for x in Rubric.objects.filter(**filters).order_by('id').values()
        ]
