from datetime import timedelta

from dbmail import send_db_mail
from django.contrib.sites.models import Site

from apps.advice.settings import ADVICE_OVERDUE_TIME


# Письмо уведомление эксперта о заявки на платную консультацию
from config.settings import SITE_PROTOCOL


def send_advice_appoint_expert_email(advice):

    ctx = {
        'username': advice.expert.get_name,
        'question_url': advice.question.get_absolute_url(),
        'question_title': advice.question.title,
        'delay_date': advice.payment_date + timedelta(minutes=ADVICE_OVERDUE_TIME),
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL
    }

    send_db_mail('advice-appoint-expert', advice.expert.email, ctx)
