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

SCENARIOS = {
    'lowprice': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'В каком городе искать отели?',
                'failure_text': 'Ошибка с городом. Попробуйте ещё раз',
                'handler': 'handle_city',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Какое количество отелей вывести (максимум 10)?',
                'failure_text': 'Ошибка с количеством. Попробуйте ещё раз',
                'handler': 'handle_numbers',
                'next_step': None
            },

        }

    },
    'highprice': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'В каком городе искать отели?',
                'failure_text': 'Ошибка с городом. Попробуйте ещё раз',
                'handler': 'handle_city',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Какое количество отелей вывести (максимум 10)?',
                'failure_text': 'Ошибка с количеством. Попробуйте ещё раз',
                'handler': 'handle_numbers',
                'next_step': None
            },

        }

    },
    'bestdeal': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'В каком городе искать отели?',
                'failure_text': 'Ошибка с городом. Попробуйте ещё раз',
                'handler': 'handle_city',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введите диапазон цен (в формате мин. цена/макс. цена',
                'failure_text': 'Ошибка с ценами. Попробуйте ещё раз',
                'handler': 'handle_price',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Введите диапазон расстояний от центра (в формате мин. расст./макс. расст.',
                'failure_text': 'Ошибка с расстояниями. Попробуйте ещё раз',
                'handler': 'handle_distance',
                'next_step': 'step4'
            },
            'step4': {
                'text': 'Какое количество отелей вывести (максимум 10)?',
                'failure_text': 'Ошибка с количеством. Попробуйте ещё раз',
                'handler': 'handle_numbers',
                'next_step': None
            },

        }
    },
}
