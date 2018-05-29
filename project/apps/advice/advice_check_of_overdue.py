import os
from django.utils import timezone

import django


def execute_command():
    from apps.advice.models import Advice
    adv = Advice.objects.filter(overdue_date__lt=timezone.now())
    for a in Advice.objects.filter(overdue_date__lt=timezone.now()):
        a.appoint_expert()
    print(adv)
    try:
        pass
    except Exception as e:
        print(e)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mlo.project.config.settings")
    django.setup()
    execute_command()
