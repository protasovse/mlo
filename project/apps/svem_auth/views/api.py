import config.error_messages as error_txt
from datetime import date
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from apps.svem_auth.models import emails
from apps.svem_system.views.api import ApiView
from apps.svem_system.exceptions import ApiPublicException
from apps.svem_auth.models.users import UserHash


class AppUser(ApiView):
    @classmethod
    def post(cls, request):
        """
        регистрация нового юзера
        """
        _email = request.POST.get('email')
        _password = request.POST.get('password')
        try:
            get_user_model().objects.get(email=_email)
            raise ApiPublicException(
                error_txt.MSG_EMAIL_USED_MSG,
                field={'field': 'email', 'txt': error_txt.MSG_EMAIL_USED_FIELD}
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
        token = UserHash.get_or_create(user)
        emails.send_activation_email(user, token)
        return True

    @classmethod
    def get(cls, request):
        _email = request.GET.get('email')
        _password = request.GET.get('password')
        # Check email
        try:
            get_user_model().objects.get(email=_email)
        except get_user_model().DoesNotExist:
            raise ApiPublicException(error_txt.MSG_EMAIL_NOT_FOUND_MSG,
                                     field={'field': 'email', 'txt': error_txt.MSG_EMAIL_NOT_FOUND_FIELD})
        # Check password
        user = authenticate(email=_email, password=_password)
        if user is None:
            raise ApiPublicException(error_txt.MSG_PASSWORD_INCORRECT_MSG,
                                     field={'field': 'password', 'txt': error_txt.MSG_PASSWORD_INCORRECT_FIELD})
        # Account not active
        if not user.is_active:
            raise ApiPublicException(error_txt.MSG_ACCOUNT_NOT_ACTIVE, code='unactive', request_status=403)
        login(request, user)
        return True


class CheckLogin(ApiView):
    @classmethod
    def get(cls, request):
        return request.user.get_data() if request.user.is_authenticated else False


class ForgotPassword(ApiView):
    @classmethod
    def post(cls, request):
        try:
            user = get_user_model().objects.get(email=request.POST.get('email'))
        except get_user_model().DoesNotExist:
            raise ApiPublicException(
                error_txt.MSG_EMAIL_NOT_FOUND_MSG,
                field={'field': 'email', 'txt': error_txt.MSG_EMAIL_NOT_FOUND_FIELD}
            )
        emails.send_forgot_email(user)


class ResetPassword(ApiView):
    @classmethod
    def post(cls, request):
        try:
            hash_obj = UserHash.objects.get(key=request.POST.get('token'), live_until__gte=date.today().isoformat())
            hash_obj.user.set_password(request.POST.get('password'))
            hash_obj.user.save()
            hash_obj.delete()
        except UserHash.DoesNotExist:
            raise ApiPublicException(error_txt.MSG_NO_CORRECT)


class ActivateAccount(ApiView):
    @classmethod
    def post(cls, request):
        try:
            hash_obj = UserHash.objects.get(key=request.POST.get('token'))
            # hash exists, but user is active already
            if hash_obj.user.is_active:
                raise ApiPublicException(error_txt.MSG_USER_IS_ACTIVE)
            # if hash exists, but too late
            if hash_obj.live_until.date() < date.today():
                raise ApiPublicException(error_txt.MSG_ACCOUNT_NOT_ACTIVE, code='unactive', request_status=403)
            user = hash_obj.user
            user.activate(True)
            hash_obj.delete()
        except UserHash.DoesNotExist:
            raise ApiPublicException(error_txt.MSG_NO_CORRECT)


class ReSend(ApiView):
    @classmethod
    def get(cls, request):
        try:
            user = get_user_model().objects.get(email=request.GET.get('email'))
            emails.send_activation_email(user)
        except get_user_model().DoesNotExist:
            hash_obj = UserHash.objects.get(key=request.GET.get('token'))
            user = hash_obj.user
            emails.send_activation_email(user)


class FlashMessageCheck(ApiView):
    @classmethod
    def get(cls, request):
        mess = messages.get_messages(request)
        if len(mess) == 0:
            return False
        for message in mess:
            # There is not method of taking first element. Why?)
            if message.level == messages.ERROR:
                raise ApiPublicException(message.message, field={'field': message.extra_tags, 'txt': message.message})
            return message.message
