from django.views.generic import DetailView, TemplateView


class Index(TemplateView):
    template_name = 'front/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_login': self.request.user.is_authenticated
        })
        return context


class RubricDetail(DetailView):
    pass
