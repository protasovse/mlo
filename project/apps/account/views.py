from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.account.forms import AccountInfoForm, UserForm


class UserEdit(FormView):
    queryset = get_user_model().objects.all()
    success_url = reverse_lazy('account:edit_regdata')

    def get_form(self):
        post = self.request.POST if self.request.method == 'POST' else None
        return UserForm(post, instance=self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profile details updated.')
        return super(UserEdit, self).form_valid(form)


class InfoEdit(FormView):
    queryset = get_user_model().objects.select_related('info').all()
    success_url = reverse_lazy('account:edit')

    def get_form(self):
        post = self.request.POST if self.request.method == 'POST' else None
        return AccountInfoForm(post, instance=self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Дополнительная информацию успешно сохранена')
        return super(InfoEdit, self).form_valid(form)
