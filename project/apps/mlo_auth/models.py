from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model

from apps.advice.models import Scheduler
from apps.mlo_auth.managers import UserManager, CLIENT, LAWYER
from apps.sxgeo.models import Cities

ROLES_CHOICES = (
    (CLIENT, _('Клиент')),
    (LAWYER, _('Юрист')),
    # (EDITOR, _('Редактор')),
)


def get_role(role_id):
    """
    role_id = 1 - это пиздец какое говно.
    Серега, не делай так!
    :param role_id:
    :return:
    """
    if role_id == CLIENT:
        return 'client'
    elif role_id == LAWYER:
        return 'lawyer'
    else:
        return None


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Электронный ящик'),
                              unique=True, db_index=True)

    first_name = models.CharField(_('first name'),
                                  max_length=32, blank=True)

    last_name = models.CharField(_('last name'),
                                 max_length=32, blank=True)

    patronymic = models.CharField(_('Отчество'),
                                  max_length=32, blank=True)

    phone = models.CharField(max_length=15, blank=True,
                             verbose_name=_('Телефон'))

    city = models.ForeignKey(Cities, on_delete=models.CASCADE,
                             blank=True, null=True,
                             verbose_name=_('Город'))

    is_staff = models.BooleanField(_('Статус персонала'),
                                   default=False,
                                   help_text=_('Указывает, может ли пользователь войти в административный сайт.'))

    is_active = models.BooleanField(_('Активный'),
                                    default=True,
                                    help_text=_('Указывает, должен ли этот пользователь считаться активным.'
                                                'Снимите этот флажок, а не удаляйте аккаунты.'))

    is_expert = models.BooleanField(_('Эксперт'),
                                    default=False,
                                    help_text=_('Указывает, является ли пользователь экспертом, имеющим право '
                                                'отвечать на платные вопросы.'))

    date_joined = models.DateTimeField(_('Дата регистрации'), auto_now_add=True)

    last_login = models.DateTimeField(_('Последний визит'), auto_now=True)

    role = models.PositiveSmallIntegerField(_('Тип учётной записи'),
                                            choices=ROLES_CHOICES, default=1, db_index=True,
                                            help_text=_('Выбирите «Юрист», если Вы оказываете юридические услуги; '
                                                        'или «Клиент», если хотите получать их.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def is_lawyer(self):
        return self.role == LAWYER

    def is_client(self):
        return self.role == CLIENT

    @property
    def about_me(self):
        p = []
        if hasattr(self, 'info') and self.info.title:
            p.append(self.info.title)
        if self.city:
            p.append(self.city.name_ru)
        return ', '.join(p)

    def get_public_data(self):
        from apps.account.models import Info
        return {
            'id': int(self.id),
            'role': get_role(self.role),
            'email': self.email,
            'full_name': self.get_full_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'patronymic': self.patronymic,
            'phone': str(self.phone),
            'city': {
                'id': self.city_id,
                'name': self.city.name_ru if self.city else None
            },
            'info': self.info.get_public_data() if hasattr(self, 'info') else Info.get_empty_data(),
            'about_me': self.about_me,
            'stat': {
                'rating': self.rating.get_rate if hasattr(self, 'rating') else None,

            },
            'url': self.get_absolute_url()
        }

    @property
    def get_full_name(self):
        if self.first_name and self.last_name and self.patronymic:
            full_name = ' '.join([self.last_name, self.first_name, self.patronymic])
        elif self.first_name:
            full_name = self.first_name
        else:
            full_name = self.email

        return full_name.strip().title()

    @property
    def get_short_name(self):
        return self.first_name

    # Имя Отчество
    @property
    def get_name(self):

        if self.first_name and self.patronymic:
            full_name = '%s %s' % (self.first_name, self.patronymic)
        elif self.first_name:
            full_name = self.first_name
        else:
            full_name = self.email

        return full_name.strip().title()

    def activate(self, do_save=True):
        if self.is_active:
            return
        self.is_active = True
        if do_save:
            self.save()

    def set_lawyer(self, do_save=True):
        if self.role == LAWYER:
            return
        self.role = LAWYER
        if do_save:
            self.save()

    def get_absolute_url(self):
        return reverse('front:lawyer_page', kwargs={'id': self.pk})

    def save(self, *args, **kwargs):
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name


class Backend(object):
    def authenticate(self, email="", password="", **kwargs):
        try:
            user = get_user_model().objects.select_related('city').get(email__iexact=email)
            if user.check_password(password):
                return user
            else:
                return None
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.select_related('city').get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
