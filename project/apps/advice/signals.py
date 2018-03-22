from django.db.models.signals import post_save

from apps.advice.models import StatusLog, Advice


def add_status_log_receiver(sender, instance, *args, **kwargs):
    """
    Добавляем запись в журнал состояний при изменении состояния консультации
    """
    c = StatusLog.objects.create(advice=instance, status=instance.status)
    c.save()


post_save.connect(add_status_log_receiver, sender=Advice)