from datetime import date
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.core.validators import EmailValidator
from django.db import IntegrityError
from apps.svem_auth.models import emails
from apps.svem_system.views.api import ApiView
from apps.svem_system.exceptions import ApiException, ApiPublicException
from apps.svem_auth.models.users import UserHash


class AppUser(ApiView):
    def post(self, request):
        """
        регистрация нового юзера
        :param request:
        :return:
        """
        try:
            _email = request.POST.get('email')
            _password = request.POST.get('password')

            validate_email = EmailValidator('ошибка: "{}" невалидный адрес электронной почты '.format(_email))
            validate_email(_email)

            try:
                get_user_model().objects.get(email=_email)

                raise ApiPublicException('Данный email уже зарегистрирован в системе')
            except get_user_model().DoesNotExist:
                pass

            user = get_user_model().objects.create_user(_email, _password)

            emails.send_activation_email(user)
            return True
        except IntegrityError:
            raise ApiException('Данный email уже зарегистрирован в системе')

    def get(self, request):
        _email = request.GET.get('email')
        _password = request.GET.get('password')
        user = authenticate(email=_email, password=_password)
        if user is None:
            raise ApiPublicException('Не удалось авторизоваться', field={'field': 'password', 'txt': 'Неверный пароль'})
        if not user.is_active:
            raise ApiPublicException(
                'Аккаунт не активирован. Вам на почту должно было придти письмо с сылкой активации акканта.'
                'Пожалуйста, проверьте почту.',
                code='unactive', request_status=403,
                field={'field': 'password', 'txt': 'неверный пароль'}
        )
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
            raise ApiPublicException('Указанный email не найден', field={'field': 'email', 'txt': 'Email не найден'})
        emails.senf_forgot_email(user)


class ResetPassword(ApiView):
    def post(self, request):
        try:
            hash = UserHash.objects.get(key=request.POST.get('token'), live_until__gte=date.today().isoformat())
            hash.user.set_password(request.POST.get('password'))
            hash.user.save()
            hash.delete()
        except UserHash.DoesNotExist:
            raise ApiPublicException(
                'Не удалось сменить пароль. Ссылка на смену пароля просрочена или некоректна',
            )


class ActivateAccount(ApiView):
    def post(self, request):
        try:
            hash = UserHash.objects.get(key=request.POST.get('token'), live_until__gte=date.today().isoformat())
            if hash.user.is_active:
                raise ApiPublicException(
                    'Не удалось активировать аккаунт. Ссылка на смену пароля просрочена или некоректна'
                )
            user = hash.user
            user.activate(False)
            user.set_lawyer()
            hash.delete()
        except UserHash.DoesNotExist:
            raise ApiPublicException('Не удалось активировать аккаунт. Ссылка на смену пароля просрочена или некоректна')


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





