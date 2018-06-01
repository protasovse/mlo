from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from apps.advice.models import Advice


class Command(BaseCommand):
    help = 'Проверяем просроченные заявки, если они есть, то переназначаем экспертов'

    def handle(self, *args, **options):

        adv = Advice.objects.filter(overdue_date__lt=timezone.now())
        for a in adv:
            a.appoint_expert()
            self.stdout.write(self.style.SUCCESS('Вопрос %d просрочен…' % a.question_id))
        else:
            self.stdout.write(self.style.SUCCESS('Просроченных заявок нет'))