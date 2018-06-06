from django.db.models.signals import post_save

from apps.advice.models import StatusLog, Advice


# Добавляем запись в журнал состояний при изменении состояния консультации
def add_status_log_receiver(sender, instance, *args, **kwargs):
    c = StatusLog.objects.create(question=instance.question, status=instance.status)
    # c.save()

post_save.connect(add_status_log_receiver, sender=Advice)
