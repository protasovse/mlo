from django.db.models.signals import post_save, pre_delete

from apps.advice.models import StatusLog, Advice, Expert, Scheduler
from apps.advice.utils import queue_add_user, queue_del_user

from apps.entry.models import Answer


# Создание новой платной консультации
def new_advice(sender, instance, *args, **kwargs):
    if 'created' in kwargs and kwargs['created']:
        instance.question.is_pay = True
        instance.question.save(update_fields=['is_pay'])
post_save.connect(new_advice, sender=Advice)


# Ответ или уточнение на платную консультацию, меняем статус на «Ответ эксперта» или «Дополнительный вопрос»
def new_answer(sender, instance, *args, **kwargs):
    if 'created' in kwargs and kwargs['created']:

        # Если ответ на платный вопрос
        if instance.on_question.is_pay:
            # Если ответ первого уровня, т.е. отвечает эксперта
            if instance.is_parent:
                # Находим консультацию эксперта, который дал ответ, если такая есть
                cur_adv = instance.on_question.advice.filter(expert=instance.author).first()
                # Если есть, то это ответ эксперта
                if cur_adv:
                    # меняем статус на «Есть ответ»
                    cur_adv.to_answered()
            # Иначе ответ — комментарий в какой-то ветке или уточнение
            else:
                # Находим консультацию эксперта, в ветке которого пользователь задал уточнение
                cur_adv = instance.on_question.advice.filter(expert=instance.parent.author).first()
                # Если есть консультация
                if cur_adv:
                    # Если пользователь — эксперт
                    if instance.author == cur_adv.expert:
                        # меняем статус на «Есть ответ»
                        cur_adv.to_answered()
                    # Если пользователь — автор вопроса
                    elif instance.author == instance.on_question.author:
                        # меняем статус на «Дополнительный вопрос»
                        cur_adv.to_addquestion()
post_save.connect(new_answer, sender=Answer)


# Добавляем пользователя в эксперты
def add_user_to_experts(sender, instance, *args, **kwargs):
    if 'created' in kwargs and kwargs['created']:
        Scheduler.objects.create(expert_id=instance.user_id)
        queue_add_user(instance.user_id)
post_save.connect(add_user_to_experts, sender=Expert)


# Удаляем пользователя из экспертов
def del_user_to_experts(sender, instance, *args, **kwargs):
    Scheduler.objects.filter(expert_id=instance.user_id).delete()
    queue_del_user(instance.user_id)
pre_delete.connect(del_user_to_experts, sender=Expert)


# Добавляем запись в журнал состояний при изменении состояния консультации
def add_status_log_receiver(sender, instance, *args, **kwargs):
    c = StatusLog.objects.create(advice=instance, status=instance.status)
    c.save()
post_save.connect(add_status_log_receiver, sender=Advice)
