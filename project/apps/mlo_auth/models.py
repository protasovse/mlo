from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model
from apps.mlo_auth.managers import UserManager, CLIENT, LAWYER

ROLES_CHOICES = (
    (CLIENT, _('Клиент')),
    (LAWYER, _('Юрист')),
    # (EDITOR, _('Редактор')),
)


# class Roles(models.Model):
#     """
#     Роли пользователей на сайте.
#     Изначально это «Юрист» или «Клиент»
#     Roles.objects.create(pk = 1, key="client", value="Клиент",
#         description="«Клиент» — это пользователь, который получает услуги", have_profile=False)
#     Roles.objects.create(pk = 2, key="lawyer", value="Юрист",
#         description="«Юрист» — это пользователь, который предоставляет услуги Клиентам", have_profile=True)
#     Roles.objects.create(pk = 3, key="editor", value="Редактор",
#         description="«Редактор» — это пользователь, который имеет право редактировать вопросы, ответы, данные пользователей", have_profile=False)
#     Юристы будут иметь профайл, Клиетны не будут иметь
#     """
#     key = models.CharField(_('Ключ на латинице'),
#                            max_length=16,
#                            unique=True)
#
#     value = models.CharField(_('Название роли'),
#                              max_length=16)
#
#     description = models.TextField(_('Описание роли'),
#                                    blank=True)
#
#     have_profile = models.BooleanField(_('Имеет ли расширенный профайл'),
#                                        default=False)
#
#     class Meta:
#         verbose_name = _('Тип учётной записи')
#         verbose_name_plural = _('Типы учётных записей')
#
#     def __str__(self):
#         return self.value


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

    last_login = models.DateTimeField(_('Последний визит'),
                                      default=timezone.now)

    role = models.PositiveSmallIntegerField(_('Тип учётной записи'),
                                            choices=ROLES_CHOICES, default=1, db_index=True,
                                            help_text=_('Выбирите «Юрист», если Вы оказываете юридические услуги; '
                                                        'или «Клиент», если хотите получать их.'))

    # role = models.ManyToManyField(Roles, verbose_name=_('Тип учётной записи'), default=1, db_index=True,
    #                               help_text=_('Выбирите «Юрист», если Вы оказываете юридические услуги; '
    #                                           'или «Клиент», если хотите получать их.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    @property
    def get_full_name(self):

        if self.first_name and self.last_name and self.patronymic:
            full_name = '%s %s %s' % (self.last_name, self.first_name, self.patronymic)
        elif self.first_name:
            full_name = self.first_name
        else:
            full_name = self.email

        return full_name.strip()

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

        return full_name.strip()

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

    def __str__(self):
        return self.get_full_name


class Backend(object):
    def authenticate(self, email="", password="", **kwargs):
        try:
            user = get_user_model().objects.get(email__iexact=email)
            if user.check_password(password):
                return user
            else:
                return None
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
