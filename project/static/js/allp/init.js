var helper;
var trigger_name = 'lead_from_widget';
helper = new _Helper;
helper.init({
    'enabled': (window.innerWidth > 600),

    'cookie_expire': 1, // in days
    'show_in_regions': ['*'],

    'style': {
        'side': 'down', // down / left / right
        'method': 'window', // inline / window

        'margin-right': '50px',
        'z-index': 10000,

        'message_sound': '/static/js/allp/message.mp3'
    },

    'consultants': [
        {
            'name': 'Олег Юрьевич',
            'profession': 'юрист',
            'userpic': '/static/js/allp/OlegYurevich.jpg'
        },
        {
            'name': 'Иван Анатольевич',
            'profession': 'адвокат',
            'userpic': '/static/js/allp/IvanAnatolevich.jpg'
        },
        {
            'name': 'Петр Павлович',
            'profession': 'адвокат',
            'userpic': '/static/js/allp/PetrPavlovich.jpg'
        }
    ],

    'template': {
        'url': '/static/js/allp/design.html',

        'vars': {
            'writing-label': 'Юрист печатает вам сообщение...',
            'input-placeholder': 'Введите ваше сообщение',
            'guarantee': 'В соответствии с ФЗ №152 мы гарантируем полную анонимность всех консультаций.',

            'window-title-1': 'МЫ ПОЛУЧИЛИ ВАШ ВОПРОС',
            'window-title-2': 'ЮРИСТ, СКОРЕЕ ВСЕГО, УЖЕ ГОТОВИТ НА НЕГО ОТВЕТ',
            'window-title-3': 'КАК НАМ МОЖНО С ВАМИ СВЯЗАТЬСЯ?',

            'window-input-label-1': 'Имя:',
            'window-input-label-2': 'Город:',
            'window-input-label-3': 'Телефон:',
            'window-input-placeholder-1': 'Ваше имя',
            'window-input-placeholder-2': 'Ваш город',

            'window-guarantee': 'В соответствии с Федеральным законом Российской Федерации от 27 июля 2006 г. N 152 "О персональных данных" - мы гарантируем полную анонимность всех консультаций.',

            'window-time-label': 'Предположительное время ответа',
            'window-time-value': '10 минут',

            'window-submit-label': 'Отправить',

            'contact-ask-name': 'Пожалуйста, представьтесь',
            'contact-ask-phone': 'Как с вами связаться?',
            'contact-name-placeholder': 'Ваше имя ...',

            'thank-you-title': 'Спасибо!',
            'thank-you-text': 'Спасибо за заявку. Наш юрист свяжется с вами в ближайшее время.'
        }
    },

    'messages': {

        'auto_messages': [
            'Здравствуйте!', 'Давайте я Вас бесплатно проконсультирую', 'Можно поподробнее?'],
        'contacts_message': 'Давайте я Вам перезвоню и проконсультирую. Так будет проще.',
        'last_message': 'Спасибо. Я свяжусь с вами в самое ближайшее время.'
    },

    'server': {

        'mode': 'ajax',
        'url_redirect': '/api/widget_send',
        // 'mode': 'redirect',
        // 'url_redirect': 'http://xn--h1abiilhh6g.xn--80asehdb/%D0%B7%D0%B0%D0%B4%D0%B0%D1%82%D1%8C-%D0%B2%D0%BE%D0%BF%D1%80%D0%BE%D1%81/?from_widget',
        // 'url_redirect': 'http://127.0.0.1:8000/%D0%B7%D0%B0%D0%B4%D0%B0%D1%82%D1%8C-%D0%B2%D0%BE%D0%BF%D1%80%D0%BE%D1%81/?from_widget',
        'params': {
            'sid': 'YTTYRDSQ8lXzoS6joPDIJvcYgHEADbvsUegBIYiF'
        },

        'event_trigger': function (trigger_name, callback) {
            // alert ('trigger_name');
            ga('send', {
                'hitType': 'event',
                'eventCategory': 'chat',
                'eventAction': trigger_name,
                'hitCallback': function () {
                    yaCounter38190105.reachGoal(trigger_name);
                    callback();
                }
            });
        }
    }
});