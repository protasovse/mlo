from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.account.forms import AccountInfoForm, UserForm, ContactsForm, EducationForm, ExperienceForm, \
    AdviceSchedulerForm


class UserEdit(FormView):
    success_url = reverse_lazy('account:edit_regdata')

    def get_form(self):
        post = self.request.POST if self.request.method == 'POST' else None
        return UserForm(post, instance=self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profile details updated.')
        return super(UserEdit, self).form_valid(form)


class InfoEdit(FormView):
    success_url = reverse_lazy('account:edit')

    def get_form(self, form_class=None):
        post = None
        files = None
        if self.request.method == 'POST':
            post = self.request.POST
            files = self.request.FILES
        return AccountInfoForm(post, files, instance=self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Дополнительная информацию успешно сохранена')
        return super(InfoEdit, self).form_valid(form)


class ContactEdit(FormView):
    success_url = reverse_lazy('account:edit_contact')

    def get_form(self, form_class=None):
        post = self.request.POST if self.request.method == 'POST' else None
        return ContactsForm(post, instance=self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Данные сохранены')
        return super(ContactEdit, self).form_valid(form)


class EducationEdit(FormView):
    success_url = reverse_lazy('account:edit_education')

    def get_form(self, form_class=None):
        post = self.request.POST if self.request.method == 'POST' else None
        return EducationForm(post, instance=self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Данные сохранены')
        return super(EducationEdit, self).form_valid(form)


class ExperienceEdit(FormView):
    success_url = reverse_lazy('account:edit_experience')

    def get_form(self, form_class=None):
        post = self.request.POST if self.request.method == 'POST' else None
        return ExperienceForm(post, instance=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ExperienceEdit, self).get_context_data(**kwargs)
        context.update({
            'stage':  self.request.user.info.stage
        })
        return context

    def form_valid(self, form):
        form.save()
        from apps.account.utils import recount_stage_on_account_info
        recount_stage_on_account_info(self.request.user.pk)
        messages.success(self.request, 'Данные сохранены')
        return super(ExperienceEdit, self).form_valid(form)


class AdviceSchedulerEdit(FormView):
    success_url = reverse_lazy('account:edit_scheduler')

    def get_form(self, form_class=None):
        post = self.request.POST if self.request.method == 'POST' else None
        return AdviceSchedulerForm(post, instance=self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Данные сохранены')
        return super(AdviceSchedulerEdit, self).form_valid(form)
