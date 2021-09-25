# -*- coding: utf-8 -*-
# сообщение для команды /help и при нераспознанном сообщении до старта сценария
HELP_ANSWER = 'Это бот для выбора отелей по заданным критериям.\n' \
              'Возможные команды:\n /lowprice — вывод самых дешёвых отелей в городе,\n' \
              ' /highprice — вывод самых дорогих отелей в городе,\n' \
              ' /bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра,\n' \
              ' /history — вывод истории поиска отелей,\n' \
              ' /help — помощь по командам бота.'
# структура соответствия допустимых команд и действий: либо сообщение в ответ на команду,
# либо название сценария, обрабатывающего эту команду
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
    },
    {
        'name': 'вывод истории поиска отелей',
        'command': '/history',
        'scenario': 'history',
        'answer': None
    }
]
# шаги, которые повторяются в нескольких сценариях
CITY_STEP = {
                'text': 'В каком городе искать отели?\n (После ввода обработка запроса может занять некоторое время.'
                        ' Всегда дожидайтесь следующего вопроса.)',
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
# структуры сценариев
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
                'text': 'Введите минимальную цену за сутки проживания',
                'failure_text': 'Неверный ввод. Только целое положительное число. Попробуйте ещё раз',
                'handler': 'handle_min_price',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Введите максимальную цену за сутки проживания',
                'failure_text': 'Только целое положительное число, больше мин. цены. Попробуйте ещё раз',
                'handler': 'handle_max_price',
                'next_step': 'step4'
            },
            'step4': {
                'text': 'Введите максимальное расстояний от центра города в км (от 1 до 9)',
                'failure_text': 'Неверное расстояние. Должно быть целое число от 1 до 9 Попробуйте ещё раз',
                'handler': 'handle_distance',
                'next_step': 'step5'
            },
            'step5': {
                'text': 'Какое количество отелей вывести (максимум 25)?',
                'failure_text': 'Неверное количество. Только цифры, число не больше 25',
                'handler': 'handle_numbers',
                'next_step': 'step6'
            },
            'step6': RESULT_STEP,
        }
    },
    'history': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Вы собираетесь узнать историю всех ваших поисков отелей.\nВыводить? (да/нет)',
                'failure_text': 'Только "да" или "нет"',
                'handler': 'handle_history',
                'next_step': 'step2'
            },
            'step2': {
                'text': '{history}\nСпасибо за обращение!',
                'failure_text': None,
                'handler': None,
                'next_step': None
            }
        }
    },
}
