from apps.advice.models import StatusLog, Advice, Scheduler
from apps.advice.utils import queue_add_user, queue_del_user


# Добавляем пользователя в эксперты
def user_to_experts(sender, instance, *args, **kwargs):
    if 'created' in kwargs:
        if instance.is_expert and instance.role == 2:
            Scheduler.objects.get_or_create(expert_id=instance.pk)
            queue_add_user(instance.pk)
        else:
            Scheduler.objects.filter(expert_id=instance.pk).delete()
            queue_del_user(instance.pk)

# post_save.connect(user_to_experts, sender=get_user_model())


# Удаляем пользователя из экспертов
# def del_user_to_experts(sender, instance, *args, **kwargs):
#     Scheduler.objects.filter(expert_id=instance.user_id).delete()
#     queue_del_user(instance.user_id)
# pre_delete.connect(del_user_to_experts, sender=Expert)


# Добавляем запись в журнал состояний при изменении состояния консультации
def add_status_log_receiver(sender, instance, *args, **kwargs):
    c = StatusLog.objects.create(advice=instance, status=instance.status)
    # c.save()

# post_save.connect(add_status_log_receiver, sender=Advice)
