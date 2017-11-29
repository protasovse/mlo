from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models

from base.mlo_auth.managers import UserManager

CLIENT = 1
LAWYER = 2
EDITOR = 3

ROLES_CHOICES = (
    (CLIENT, _('Клиент')),
    (LAWYER, _('Юрист')),
    (EDITOR, _('Редактор'))
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Электронный ящик'),
                              unique=True, db_index=True)

    first_name = models.CharField(_('first name'),
                                  max_length=32, blank=True)

    last_name = models.CharField(_('last name'),
                                 max_length=32, blank=True)

    patronymic = models.CharField(_('Отчество'),
                                  max_length=32, blank=True)

    is_staff = models.BooleanField(_('Статус персонала'),
                                   default=False,
                                   help_text=_('Указывает, может ли пользователь войти в административный сайт.'))

    is_active = models.BooleanField(_('Активный'),
                                    default=True,
                                    help_text=_('Указывает, должен ли этот пользователь считаться активным.'
                                                'Снимите этот флажок, а не удаляйте аккаунты.'))

    date_joined = models.DateTimeField(_('Дата регистрации'),
                                       default=timezone.now)

    role = models.PositiveSmallIntegerField(_('Тип учётной записи'),
                                            choices=ROLES_CHOICES, default=1, db_index=True,
                                            help_text=_('Выбирите «Юрист», если Вы оказываете юридические услуги; '
                                                        'или «Клиент», если хотите получать их.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    @property
    def get_full_name(self):

        if self.first_name and self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
        elif self.first_name:
            full_name = self.first_name
        else:
            full_name = self.email

        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
