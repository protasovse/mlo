from apps.svem_system.exceptions import ApiPublicException
from apps.svem_auth.models.users import UserHash
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date


def send_activation_email(user):
    if user.is_active:
        raise ApiPublicException(
            'Активационное письмо не было отправлено: Пользователь уже активирован.'
        )

    token = UserHash.get_or_create(user)

    ctx = {
        'hash': token.key,
        'user': user,
        'site': Site.objects.get_current(),
        'protocol': settings.SITE_PROTOCOL
    }

    message = render_to_string('emails/auth/activation.html', ctx)
    msg = EmailMessage('Подвердите аккаунт', message, to=[user.email])
    msg.content_subtype = 'html'
    msg.send()


def senf_forgot_email(user):
    try:
        user_hash = UserHash.objects.get(user=user, live_until__gte=date.today().isoformat())
    except UserHash.DoesNotExist:
        user_hash = UserHash(user=user)
        user_hash.save()

    ctx = {
        'hash': user_hash,
        'user': user,
        'site': Site.objects.get_current(),
        'protocol': 'http'
    }

    message = render_to_string('emails/auth/forgot.html', ctx)
    msg = EmailMessage('восстановление пароля', message, to=[user.email])
    msg.content_subtype = 'html'
    msg.send()