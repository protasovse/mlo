from django.db.models.signals import post_save, pre_delete

from apps.advice.models import StatusLog, Advice, Expert, Scheduler
from apps.advice.utils import queue_add_user, queue_del_user


def add_user_to_experts(sender, instance, *args, **kwargs):
    """
    Добавляем пользователя в эксперты
    """
    if 'created' in kwargs and kwargs['created']:
        Scheduler.objects.create(expert_id=instance.user_id)
        queue_add_user(instance.user_id)

post_save.connect(add_user_to_experts, sender=Expert)


def del_user_to_experts(sender, instance, *args, **kwargs):
    """
    Удаляем пользователя из экспертов
    """
    Scheduler.objects.filter(expert_id=instance.user_id).delete()
    queue_del_user(instance.user_id)

pre_delete.connect(del_user_to_experts, sender=Expert)


def add_status_log_receiver(sender, instance, *args, **kwargs):
    """
    Добавляем запись в журнал состояний при изменении состояния консультации
    """
    c = StatusLog.objects.create(advice=instance, status=instance.status)
    c.save()


post_save.connect(add_status_log_receiver, sender=Advice)