from dbmail import send_db_mail

from apps.svem_system.exceptions import ApiPublicException
from apps.svem_auth.models.users import UserHash
from django.contrib.sites.models import Site
from datetime import date

from config.settings import SITE_PROTOCOL


def send_activation_email(user):

    if user.is_active:
        raise ApiPublicException(
            'Активационное письмо не было отправлено: Пользователь уже активирован.'
        )

    token = UserHash.get_or_create(user)

    ctx = {
        'hash': token.key,
        'username': user.get_name,
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL
    }

    send_db_mail(
        'sign-up',
        user.email,
        ctx,
    )


def send_forgot_email(user):

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

    send_db_mail(
        'vosstanovlenie-parolya',
        user.email,
        ctx,
    )
