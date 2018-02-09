from datetime import date
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from apps.svem_auth.models import emails
from apps.svem_system.views.api import ApiView
from apps.svem_system.exceptions import ApiPublicException
from apps.svem_auth.models.users import UserHash

MSG_EMAIL_NOT_VALID = '«{}» — неверный адрес электронной почты'
MSG_EMAIL_USED_FIELD = 'Этот электронный ящик уже используется'
MSG_EMAIL_USED_MSG = 'Введённый электронный ящик уже используется другим пользователем.'
MSG_EMAIL_NOT_FOUND_FIELD = 'Электронный ящик не найден'
MSG_EMAIL_NOT_FOUND_MSG = 'Введенный вами электронный ящик не зарегистрирован. ' \
                          'Проверьте правильность ввода или пройдите регистрацию.'
MSG_PASSWORD_INCORRECT_MSG = 'К сожалению, вы ввели неверный пароль. Проверьте свой пароль еще раз.'
MSG_PASSWORD_INCORRECT_FIELD = 'Неверный пароль'
MSG_PASSWORD_STRENGTH = 'Пароль недостаточно сложный'
MSG_DATA_NOT_VALID = 'Введите правильные данные'
MSG_NO_CORRECT = 'Не удалось активировать учётную запись. Ссылка на смену пароля просрочена или неверна.'
MSG_ACCOUNT_NOT_ACTIVE = 'Учётная запись не активна. ' \
                         'Вам на почту ранее было отправлено письмо с ссылкой для активации акканта.'
MSG_USER_IS_ACTIVE = 'Активация аккаунта не требуется. Аккаунт уже активирован'


class PasswordValidator:
    message = MSG_PASSWORD_STRENGTH
    strength_len = 6

    def __init__(self, message=None, code=None, strength_len=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if strength_len is not None:
            self.strength_len = strength_len

    def __call__(self, value):
        if len(value) < self.strength_len:
            raise ValidationError(self.message, code=self.code)


class AppUser(ApiView):

    def post(self, request):
        """
        регистрация нового юзера
        """
        try:
            _email = request.POST.get('email')
            _password = request.POST.get('password')

            validate_email = EmailValidator(MSG_EMAIL_NOT_VALID.format(_email), 'email')
            validate_password = PasswordValidator(MSG_PASSWORD_STRENGTH, 'password')

            validate_email(_email)
            validate_password(_password)
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
            hash = UserHash.objects.get(key=request.POST.get('token'))
            # hash exists, but user is active already
            if hash.user.is_active:
                raise ApiPublicException(MSG_USER_IS_ACTIVE)
            # if hash exists, but too late
            if hash.live_until.date() < date.today():
                raise ApiPublicException(MSG_ACCOUNT_NOT_ACTIVE, code='unactive', request_status=403)
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
            hash = UserHash.objects.get(key=request.GET.get('token'))
            user = hash.user
            emails.send_activation_email(user)


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





