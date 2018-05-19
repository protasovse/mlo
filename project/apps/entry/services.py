from django.db import transaction
from django.db.models import F
from apps.entry.models import Answer, Additionals
from apps.question.emails import send_question_new_answer
from apps.rating.models import RatingScore, Type, RatingScoreComment
from apps.rating.utils import add_score
from apps.svem_system.exceptions import BackendPublicException


def answer(question, content, user, parent_id=None):
    """
    Добавляем ответ на вопрос
    :param question:
    :param content:
    :param user:
    :param parent_id:
    :return: созданный ответ
    """
    if int(parent_id) == 0:
        parent_id = None

    if not user.is_authenticated:
        raise BackendPublicException("You can't answer")

    if parent_id is None and not user.is_lawyer():
        raise BackendPublicException("You can't answer. Only lawyer")

    if parent_id is None and question.get_answers().filter(author_id=user.id, parent=None).count():
        raise BackendPublicException("You can't answer. There are your answers in the question")

    advice = question.advice if hasattr(question, 'advice') else None

    # create an answer
    instance = Answer.objects.create(
        on_question=question,
        author_id=user.id,
        content=content,
        parent_id=parent_id,
    )

    # update reply counter on entry
    if parent_id:
        _ifu = instance.parent
    else:
        _ifu = question
    _ifu.reply_count = F('reply_count') + 1
    _ifu.save(update_fields=['reply_count'])

    # Добавляем балл рейтинга
    if user.is_lawyer():
        if instance.parent is None:  # Если первый ответ
            score = RatingScore.objects.create(type=Type.objects.get(key='answer'), user=instance.author)
            RatingScoreComment.objects.create(rating_score=score, comment='За ответ %d' % (instance.pk,))
        # если дополнительный ответ
        else:
            score = RatingScore.objects.create(type=Type.objects.get(key='add_answer'), user=instance.author)
            RatingScoreComment.objects.create(rating_score=score, comment='За уточнение %d' % (instance.pk,))
        # Добавляем балл к рейтингу
        add_score(instance.author.pk, score.type.value)
        send_question_new_answer(question, instance)
        # Уведомление — «Юрист ответил на Ваш вопрос»

    # Обновляем answer_count на account_info (кеш количества ответов юриста)
    # считаем только ответы первого уровня
    if user.is_lawyer():
        if instance.parent is None:  # Если первый ответ
            user.info.answer_count = F('answer_count') + 1
            user.info.save(update_fields=['answer_count'])

    # Запись в таблице уточненеий
    # Если дополнительный вопрос «клиента»
    if parent_id and user.is_client():
        Additionals.objects.get_or_create(question_id=question.pk, user_id=instance.parent.author_id)
        # Уведомление — «Клиент задал дополнительный вопрос на ответ юриста»
    elif parent_id and user.is_lawyer() and user == instance.parent.author:  # если отвечает тот юрист, чья ветка
        Additionals.objects.filter(question_id=question.pk, user_id=instance.parent.author_id).delete()

    ''' 
    Платные вопросы Advice 
    Уведомления юриста и клиента находятся в методах: to_answered и to_addquestion
    '''
    if advice:
        if user == advice.expert:  # Если отвечает юрист, который ведёт консультацию
            advice.to_answered()
        elif user == question.author:  # Если пишет автор вопроса
            advice.to_addquestion()

    return instance
