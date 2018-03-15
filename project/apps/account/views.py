from django.contrib.auth import get_user_model
from django.views.generic import TemplateView


class AccountDetail(TemplateView):
    # queryset = get_user_model().objects.all()

    def get_context_data(self, **kwargs):
        context = super(AccountDetail, self).get_context_data(**kwargs)
        context['user'] = get_user_model().objects.select_related('info').get(pk=self.request.user.pk)
        return context
