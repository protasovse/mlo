from collections import OrderedDict
from datetime import timedelta
from urllib.parse import urlencode

import requests
from dbmail import send_db_mail, send_db_sms
from django.contrib.sites.models import Site
from requests.auth import HTTPBasicAuth

from apps.advice.settings import ADVICE_OVERDUE_TIME, EXPERT_FEE_IN_PERCENT
from apps.entry.models import Answer

from config.settings import SITE_PROTOCOL


# Письмо уведомление эксперта о заявки на платную консультацию
def send_advice_appoint_expert_email(advice):

    ctx = {
        'username': advice.expert.get_name,
        'advice': advice,
        'delay_date': advice.payment_date + timedelta(minutes=ADVICE_OVERDUE_TIME),
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL
    }

    send_db_mail('advice-appoint-expert', advice.expert.email, ctx)
    # send_db_sms('advice-sms-appoint-expert', advice.expert.phone, ctx)

    '''
    long_url = '{protocol}://{site}{url}'.format(
        protocol=SITE_PROTOCOL,
        site=Site.objects.get_current(),
        url=advice.question.get_absolute_url()
    )

    api_url = 'https://www.googleapis.com/urlshortener/v1/url'
    api_key = 'AIzaSyD7GJizTAQaQ3C0v_ysFTJz2HWZMopHb5E'
    r = requests.post(
        "{api_url}?key={api_key}".format(api_url=api_url, api_key=api_key),
        json={'longUrl': long_url}
    )
    short_url = r.json()['id']

    url = 'http://api.iqsms.ru/messages/v2/send/'
    params = OrderedDict([
        ('phone', '+79265380040'),
        ('text', 'Вам платная заявка: {short_url}. Принять в течении {min} мин.'.format(
            short_url=short_url,
            min=ADVICE_OVERDUE_TIME
        )),
        ('sender', 'YURIST24')
    ])

    r = requests.get(
        url,
        auth=('z1522654896889', '972276'),
        params=urlencode(params)
    )
    '''


def send_advice_to_in_work_to_client_message(advice, num_hours):

    ctx = {
        'username': advice.question.author.get_name,
        'expert': advice.expert,
        'question_url': advice.question.get_absolute_url(),
        'num_hours': num_hours,
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL
    }

    send_db_mail('advice-to-in-work-to-client-message', advice.question.author.email, ctx)


def send_advice_new_answer(advice):

    ctx = {
        'username': advice.question.author.get_name,
        'advice': advice,
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL
    }

    send_db_mail('advice-new-answer', advice.question.author.email, ctx)


# Протестировать!
def send_advice_additional_question(advice):

    ctx = {
        'username': advice.expert.get_name,
        'advice': advice,
        'last_answer': Answer.objects.filter(on_question=advice.question, author=advice.question.author).last(),
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL
    }

    send_db_mail('advice-additional-question', advice.expert.email, ctx)


def send_advice_closed(advice):

    ctx = {
        'username': advice.question.author.get_name,
        'advice': advice,
        'fee': advice.cost*EXPERT_FEE_IN_PERCENT/100,
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL
    }

    send_db_mail('advice-closed-to-expert-message', advice.question.author.email, ctx)