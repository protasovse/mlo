from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.utils import timezone

from apps.advice.models import StatusLog, Advice, Scheduler
from apps.advice.utils import queue_add_user, queue_del_user

from apps.entry.models import Answer, Question
from config.settings import ADVICE_COST


# Создание новой платной консультации
def new_advice(sender, instance, *args, **kwargs):
    if 'created' in kwargs and kwargs['created'] and instance.is_pay:
        Advice.objects.get_or_create(question=instance, cost=ADVICE_COST)

# post_save.connect(new_advice, sender=Question)


# Ответ или уточнение на платную консультацию, меняем статус на «Ответ эксперта» или «Дополнительный вопрос»
def new_answer_for_advice(sender, instance, *args, **kwargs):
    if 'created' in kwargs and kwargs['created']:

        # Если ответ на платный вопрос
        if instance.on_question.is_pay:
            if hasattr(instance.on_question, 'advice'):
                cur_adv = instance.on_question.advice

                if instance.is_parent:  # Если ответ первого уровня, т.е. отвечает эксперт
                    cur_adv.to_answered()

                else:  # Иначе ответ — комментарий в какой-то ветке или уточнение
                    # Если пользователь — эксперт
                    if instance.author == instance.parent.author:
                        # меняем статус на «Есть ответ»
                        cur_adv.to_answered()
                    # Если пользователь — автор вопроса
                    elif instance.author == instance.on_question.author:
                        # меняем статус на «Дополнительный вопрос»
                        cur_adv.to_addquestion()

# post_save.connect(new_answer_for_advice, sender=Answer)


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
