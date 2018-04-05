import hashlib

from django.http import HttpResponse
from django.shortcuts import render

SECRET = 'bhpC6s2sVFnJQF8l/b3K9nV0'


def advice_to_payment_confirmed(request):

    """
    ?operation_id=904035776918098009&notification_type=p2p-incoming&datetime=2014-04-28T16:31:28Z&sha1_hash=9d9f21efc89f44a8d5125e5360a8194e1e292e2a&sender=41003188981230&codepro=false&currency=643&amount=0.99&withdraw_amount=1.00&label=advice.456456
    9d9f21efc89f44a8d5125e5360a8194e1e292e2a
    9d9f21efc89f44a8d5125e5360a8194e1e292e2a
    """

    data = request.GET

    result_string = "&".join((
        data['notification_type'],
        data['operation_id'],
        data['amount'],
        data['currency'],
        data['datetime'],
        data['sender'],
        data['codepro'],
        SECRET,
        data['label']
    ))

    sha = hashlib.sha1(result_string.encode()).hexdigest()

    print(sha)
    print(data['sha1_hash'])

    if sha == data['sha1_hash']:

        # Пример label=advice.456456
        question_id = data['label'].split('.')[1]
        label = data['label'].split('.')[0]

    return HttpResponse(sha)
