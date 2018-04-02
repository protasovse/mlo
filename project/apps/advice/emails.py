from datetime import timedelta

from dbmail import send_db_mail
from django.contrib.sites.models import Site

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