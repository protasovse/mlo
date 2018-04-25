from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F

from apps.entry.models import Answer, Question, Additionals
from apps.rating.models import RatingScore, Type, RatingScoreComment
from apps.rating.utils import add_score


def answer(question_id, content, author_id, parent_id=None):
    """
    Добавляем ответ на вопрос
    :param question_id:
    :param content:
    :param author_id:
    :param parent_id:
    :return: созданный ответ
    """

    if parent_id is None and Answer.objects.filter(on_question=question_id, author_id=author_id, parent=None).count():
        raise ValueError('На этот вопрос пользователь уже отвечал')

    question = Question.objects.get(pk=question_id)
    author = get_user_model().objects.get(pk=author_id)

    advice = question.advice if hasattr(question, 'advice') else None

    if parent_id is None and author.role == 1:
        raise ValueError('Только юрист может отвечать на вопрос')

    with transaction.atomic():
        # create an answer
        instance = Answer.objects.create(
            on_question=question,
            author=author,
            content=content,
            parent_id=parent_id,
        )

        # update thread_id
        instance.thread = parent_id if parent_id else instance.pk
        instance.save(update_fields=['thread'])

        # update reply counter on entry
        if parent_id:
            _ifu = instance.parent
        else:
            _ifu = question
        _ifu.reply_count = F('reply_count') + 1
        _ifu.save(update_fields=['reply_count'])

        # Добавляем балл рейтинга
        if author.role == 2:
            if instance.parent is None:  # Если первый ответ
                score = RatingScore.objects.create(type=Type.objects.get(key='answer'), user=instance.author)
                RatingScoreComment.objects.create(rating_score=score, comment='За ответ %d' % (instance.pk,))
            # если дополнительный ответ
            else:
                score = RatingScore.objects.create(type=Type.objects.get(key='add_answer'), user=instance.author)
                RatingScoreComment.objects.create(rating_score=score, comment='За уточнение %d' % (instance.pk,))
            # Добавляем балл к рейтингу
            add_score(instance.author.pk, score.type.value)
            # Уведомление — «Юрист ответил на Ваш вопрос»

        # Обновляем answer_count на account_info (кеш количества ответов юриста)
        # считаем только ответы первого уровня
        if author.role == 2:
            if instance.parent is None:  # Если первый ответ
                author.info.answer_count = F('answer_count') + 1
                author.info.save(update_fields=['answer_count'])

        # Запись в таблице уточненеий
        # Если дополнительный вопрос «клиента»
        if parent_id and author.role == 1:
            Additionals.objects.create(question_id=question.pk, user_id=instance.parent.author_id)
            # Уведомление — «Клиент задал дополнительный вопрос на ответ юриста»
        elif parent_id and author.role == 2 and author == instance.parent.author:  # если отвечает тот юрист, чья ветка
            Additionals.objects.filter(question_id=question.pk, user_id=instance.parent.author_id).delete()

        ''' 
        Платные вопросы Advice 
        Уведомления юриста и клиента находятся в методах: to_answered и to_addquestion
        '''
        if advice:
            if author == advice.expert:  # Если отвечает юрист, который ведёт консультацию
                advice.to_answered()
            elif author == question.author:  # Если пишет автор вопроса
                advice.to_addquestion()

    return instance
