from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import EmailValidator
from apps.svem_auth.models.users import PasswordValidator
from django.utils.translation import ugettext_lazy as _

CLIENT = 1
LAWYER = 2
# EDITOR = 3

MSG_EMAIL_NOT_VALID = '«{}» — неверный адрес электронной почты'
MSG_PASSWORD_STRENGTH = 'Пароль недостаточно сложный'


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_('Пользователь должен иметь электронный ящик'))

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):

        validate_email = EmailValidator(MSG_EMAIL_NOT_VALID.format(email), 'email')
        validate_password = PasswordValidator(MSG_PASSWORD_STRENGTH, 'password')

        validate_email(email)
        validate_password(password)

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

    def lawyers(self):
        return super(UserManager, self).filter(role=LAWYER)
