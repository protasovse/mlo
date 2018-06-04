from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone
from apps.advice.models import Advice, ADVICE_PAYMENT_CONFIRMED
from apps.entry.managers import PUBLISHED


class Command(BaseCommand):
    help = 'Проверяем просроченные заявки, если они есть, то переназначаем экспертов'

    def handle(self, *args, **options):
        print(timezone)
        adv = Advice.objects.filter(question__status=PUBLISHED).\
            filter(status=ADVICE_PAYMENT_CONFIRMED).\
            filter(Q(overdue_date__lt=timezone.now()) | Q(overdue_date=None))
        for a in adv:
            a.appoint_expert()
            self.stdout.write(self.style.SUCCESS('Вопрос %d просрочен…' % a.question_id))
        else:
            self.stdout.write(self.style.SUCCESS('Просроченных заявок нет'))