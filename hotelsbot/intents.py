HELP_ANSWER = 'Возможные команды: /lowprice — вывод самых дешёвых отелей в городе,' \
              ' /highprice — вывод самых дорогих отелей в городе,' \
              ' /bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра,' \
              ' /help — помощь по командам бота'

INTENTS = [
    {
        'name': 'помощь по командам бота',
        'command': '/help',
        'scenario': None,
        'answer': HELP_ANSWER
    },
    {
        'name': 'вывод самых дешёвых отелей в городе',
        'command': '/lowprice',
        'scenario': 'lowprice',
        'answer': None
    },
    {
        'name': 'вывод самых дорогих отелей в городе',
        'command': '/highprice',
        'scenario': 'highprice',
        'answer': None
    },
    {
        'name': 'вывод отелей, наиболее подходящих по цене и расположению от центра',
        'command': '/bestdeal',
        'scenario': 'bestdeal',
        'answer': None
    }
]

CITY_STEP = {
                'text': 'В каком городе искать отели?',
                'failure_text': 'В нашей базе нет отелей для этого города. Попробуйте ввести другой город',
                'handler': 'handle_city',
                'next_step': 'step2'
            }


NUMBERS_STEP = {
                'text': 'Какое количество отелей вывести (максимум 25)?',
                'failure_text': 'Неверное количество. Только цифры, число не больше 25',
                'handler': 'handle_numbers',
                'next_step': 'step3'
            }

RESULT_STEP = {
                'text': 'Список  отелей по вашему запросу:\n{hotels}\nСпасибо за обращение!',
                'failure_text': None,
                'handler': None,
                'next_step': None
            }

SCENARIOS = {
    'lowprice': {
        'first_step': 'step1',
        'steps': {
            'step1': CITY_STEP,
            'step2': NUMBERS_STEP,
            'step3': RESULT_STEP
        }
    },
    'highprice': {
        'first_step': 'step1',
        'steps': {
            'step1': CITY_STEP,
            'step2': NUMBERS_STEP,
            'step3': RESULT_STEP,
        }
    },
    'bestdeal': {
        'first_step': 'step1',
        'steps': {
            'step1': CITY_STEP,
            'step2': {
                'text': 'Введите диапазон цен (в формате мин. цена/макс. цена',
                'failure_text': 'Ошибка с ценами. Попробуйте ещё раз',
                'handler': 'handle_price',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Введите максимальное расстояний от центра города',
                'failure_text': 'Ошибка с расстоянием. Попробуйте ещё раз',
                'handler': 'handle_distance',
                'next_step': 'step4'
            },
            'step4': {
                'text': 'Какое количество отелей вывести (максимум 25)?',
                'failure_text': 'Неверное количество. Только цифры, число не больше 25',
                'handler': 'handle_numbers',
                'next_step': 'step5'
            },
            'step5': RESULT_STEP,
        }
    },
}
