import hashlib

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from apps.advice.models import Advice
from apps.entry.models import Question
from config.settings import MONEY_YANDEX_SECRET


@csrf_exempt
def advice_to_payment_confirmed(request):
    """
    http://мойюрист.онлайн/advice/to_payment_confirmed — url подтверждения
    ?operation_id=904035776918098009&notification_type=p2p-incoming&datetime=2014-04-28T16:31:28Z&sha1_hash=8cd2341395aa45f4bfe1f5d5079b878949d3e3cc&sender=41003188981230&codepro=false&currency=643&amount=800.00&withdraw_amount=800.00&label=advice.1500026
    8cd2341395aa45f4bfe1f5d5079b878949d3e3cc
    """

    import sys
    sys.stdout = open('/tmp/payment.log', 'w')
    print("Тест55")
    print(request.POST)
    print(request.GET)
    print(request)
    sys.stdout.close()

    resp = ''
    # data = request.GET
    data = request.POST

    if not request.POST:
        return HttpResponse('Нет данных')

    try:
        result_string = "&".join((
            data['notification_type'],
            data['operation_id'],
            data['amount'],
            data['currency'],
            data['datetime'],
            data['sender'],
            data['codepro'],
            MONEY_YANDEX_SECRET,
            data['label']
        ))
    except MultiValueDictKeyError:
        return HttpResponse('Неверные данные')

    sha = hashlib.sha1(result_string.encode()).hexdigest()
    # print(sha)

    if sha == data['sha1_hash']:

        # Пример label=advice.456456
        label = data['label'].split('.')[0]

        if label == 'advice':
            question_id = data['label'].split('.')[1]
            question = get_object_or_404(Question, pk=question_id)
            question.pay()
            advice = Advice.objects.get(question_id=question_id)

            if advice.to_payment_confirmed():
                # Обновляем цену оплаченную по факту
                if 'withdraw_amount' in data:
                    advice.cost = int(float(data['withdraw_amount']))
                    advice.save(update_fields=['cost'])

                resp = 'Платёж подтверждён, вопрос: {}'.format(question_id)
            else:
                resp = 'Не удалось обновить статус завки'

    else:
        resp = 'Хеш неверен! Проверьте секретное слово'

    return HttpResponse(resp)
