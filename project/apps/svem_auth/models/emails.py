from dbmail import send_db_mail

from apps.svem_system.exceptions import ApiPublicException
from apps.svem_auth.models.users import UserHash
from django.contrib.sites.models import Site
from datetime import date

from config.settings import SITE_PROTOCOL


def send_activation_email(user, token):
    if user.is_active:
        raise ApiPublicException(
            'Активационное письмо не было отправлено: Пользователь уже активирован.'
        )

    ctx = {
        'hash': token.key,
        'username': user.get_name,
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL
    }

    send_db_mail('activation', user.email, ctx)


def send_forgot_password_email(user):

    try:
        user_hash = UserHash.objects.get(user=user, live_until__gte=date.today().isoformat())
    except UserHash.DoesNotExist:
        user_hash = UserHash(user=user)
        user_hash.save()

    ctx = {
        'hash': user_hash,
        'username': user.get_name,
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL,
    }

    send_db_mail('forgot-password', user.email, ctx)


def send_confirm_question(user, question, token, email, password):
    ctx = {
        'hash': token,
        'username': user.get_name,
        'question_url': question.get_absolute_url(),
        'question_title': question.title,
        'question_content': question.content,
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL,
        'email': email,
        'password': password,
    }

    send_db_mail('confirm-question', user.email, ctx)


def send_paid_question(user, question, email, password):
    ctx = {
        'username': user.get_name,
        'question_url': question.get_absolute_url(),
        'question_title': question.title,
        'question_content': question.content,
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL,
        'email': email,
        'password': password,
    }
    send_db_mail('paid-question', user.email, ctx)
