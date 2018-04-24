from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory, Textarea, DateInput, RadioSelect, TimeInput
from django_select2.forms import ModelSelect2Widget
from image_cropping import ImageCropWidget
from phonenumber_field.formfields import PhoneNumberField

from apps.account.models import Info, Contact, Education, Experience
from apps.advice.models import Scheduler
from apps.sxgeo.models import Cities, Country


class UserForm(forms.ModelForm):
    """
    Основная информация пользователя
    """

    last_name = forms.CharField(required=True, label='Фамилия')
    first_name = forms.CharField(required=True, label='Имя')
    phone = PhoneNumberField(label='Телефон')

    def save(self, commit=True):
        return super(UserForm, self).save(commit)

    class Meta:
        model = get_user_model()
        fields = ('last_name', 'first_name', 'patronymic', 'phone', 'city', )
        widgets = {
            'city': ModelSelect2Widget(
                model=Cities,
                search_fields=['name_ru__istartswith'],
            ),
        }


AccountInfoForm = inlineformset_factory(
    get_user_model(), Info,
    fields=('orig', 'photo', 'pic', 'birth_date', 'sex', 'title', 'short', 'about', 'signature', ),
    can_delete=False,
    widgets={
        'signature': Textarea(attrs={'rows': 3}),
        'short': Textarea(attrs={'rows': 4}),
        'status': Textarea(attrs={'rows': 2}),
        'birth_date': DateInput(),
        'sex': RadioSelect(),
    }
)


ContactsForm = inlineformset_factory(
    get_user_model(), Contact,
    can_delete=True,
    fields=('type', 'value', )
)


EducationForm = inlineformset_factory(
    get_user_model(), Education,
    can_delete=True,
    fields=('name', 'faculty', 'specialty', 'finish', 'diplom', ),
    extra=1
)

ExperienceForm = inlineformset_factory(
    get_user_model(), Experience,
    can_delete=True,
    fields=('name', 'position', 'description', 'site', 'start', 'finish', ),
    extra=1
)

AdviceSchedulerForm = inlineformset_factory(
    get_user_model(), Scheduler,
    can_delete=False,
    fields=('is_available', 'begin', 'end', 'weekend', ),
    widgets=({
        'begin': TimeInput(),
        'end': TimeInput(),
    })
)

