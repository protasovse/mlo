from dbmail import send_db_mail
from django.contrib.sites.models import Site

from config.settings import SITE_PROTOCOL


def send_question_new_answer(question, answer):

    ctx = {
        'username': question.author.get_name,
        'question': question,
        'answer': answer,
        'site': Site.objects.get_current(),
        'protocol': SITE_PROTOCOL
    }

    send_db_mail('question-new-answer', question.author.email, ctx)


