from datetime import date
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.mlo_auth.managers import LAWYER
from apps.svem_auth.models import emails
from apps.svem_system.views.api import ApiView
from apps.svem_system.exceptions import ApiException, ApiPublicException
from apps.svem_auth.models.users import UserHash

MSG_EMAIL_NOT_VALID = '«{}» — неверный адрес электронной почты'
MSG_EMAIL_USED_FIELD = 'Этот электронный ящик уже используется'
MSG_EMAIL_USED_MSG = 'Введённый электронный ящик уже используется другим пользователем.'
MSG_EMAIL_NOT_FOUND_FIELD = 'Электронный ящик не найден'
MSG_EMAIL_NOT_FOUND_MSG = 'Введенный вами электронный ящик не зарегистрирован. ' \
                          'Проверьте правильность ввода или пройдите регистрацию.'
MSG_PASSWORD_INCORRECT_MSG = 'К сожалению, вы ввели неверный пароль. Проверьте свой пароль еще раз.'
MSG_PASSWORD_INCORRECT_FIELD = 'Неверный пароль'
MSG_DATA_NOT_VALID = 'Введите правильные данные'
MSG_NO_CORRECT = 'Не удалось активировать учётную запись. Ссылка на смену пароля просрочена или неверна.'
MSG_ACCOUNT_NOT_ACTIVE = 'Учётная запись не активна. ' \
                         'Вам на почту ранее было отправлено письмо с ссылкой для активации акканта.'


class AppUser(ApiView):

    def post(self, request):
        """
        регистрация нового юзера
        """
        try:
            _email = request.POST.get('email')
            _password = request.POST.get('password')
            validate_email = EmailValidator(
                MSG_EMAIL_NOT_VALID.format(_email),
                'email'
            )
            validate_email(_email)
            try:
                get_user_model().objects.get(email=_email)
                raise ApiPublicException(
                    MSG_EMAIL_USED_MSG,
                    field={'field': 'email', 'txt': MSG_EMAIL_USED_FIELD}
                )
            except get_user_model().DoesNotExist:
                pass
            user = get_user_model().objects.create_user(
                _email, _password,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                patronymic=request.POST.get('patronymic')
            )
            user.set_lawyer()
            emails.send_activation_email(user)
            return True
        except ValidationError as err:
            raise ApiPublicException(
                MSG_DATA_NOT_VALID,
                field={'field': err.code, 'txt': err.message}
            )

    def get(self, request):
        _email = request.GET.get('email')
        _password = request.GET.get('password')
        # Check email
        try:
            get_user_model().objects.get(email=_email)
        except get_user_model().DoesNotExist:
            raise ApiPublicException(MSG_EMAIL_NOT_FOUND_MSG,
                                     field={'field': 'email', 'txt': MSG_EMAIL_NOT_FOUND_FIELD})
        # Check password
        user = authenticate(email=_email, password=_password)
        if user is None:
            raise ApiPublicException(MSG_PASSWORD_INCORRECT_MSG,
                                     field={'field': 'password', 'txt': MSG_PASSWORD_INCORRECT_FIELD})
        # Account not active
        if not user.is_active:
            raise ApiPublicException(MSG_ACCOUNT_NOT_ACTIVE, code='unactive', request_status=403)
        login(request, user)
        return True


class CheckLogin(ApiView):
    def get(self, request):
        return request.user.is_authenticated


class ForgotPassword(ApiView):
    def post(self, request):
        try:
            user = get_user_model().objects.get(email=request.POST.get('email'))
        except get_user_model().DoesNotExist:
            raise ApiPublicException(MSG_EMAIL_NOT_FOUND_MSG,
                                     field={'field': 'email', 'txt': MSG_EMAIL_NOT_FOUND_FIELD})
        emails.send_forgot_email(user)


class ResetPassword(ApiView):
    def post(self, request):
        try:
            hash = UserHash.objects.get(key=request.POST.get('token'), live_until__gte=date.today().isoformat())
            hash.user.set_password(request.POST.get('password'))
            hash.user.save()
            hash.delete()
        except UserHash.DoesNotExist:
            raise ApiPublicException(MSG_NO_CORRECT)


class ActivateAccount(ApiView):
    def post(self, request):
        try:
            hash = UserHash.objects.get(key=request.POST.get('token'), live_until__gte=date.today().isoformat())
            if hash.user.is_active:
                raise ApiPublicException(MSG_NO_CORRECT)
            user = hash.user
            user.activate(True)
            hash.delete()
        except UserHash.DoesNotExist:
            raise ApiPublicException(MSG_NO_CORRECT)


class ReSend(ApiView):
    def get(self, request):
        try:
            user = get_user_model().objects.get(email=request.GET.get('email'))
            emails.send_activation_email(user)
        except get_user_model().DoesNotExist:
            raise ApiPublicException('Не удалось отправить активационное письмо')


class FlashMessageCheck(ApiView):
    def get(self, request):
        mess = messages.get_messages(request)

        if len(mess) == 0:
            return False
        for message in mess:
            # почему-то нет интерфейса получения первого элмента
            if message.level == messages.ERROR:
                raise ApiPublicException(message.message, field={'field': message.extra_tags, 'txt': message.message})
            return message.message





