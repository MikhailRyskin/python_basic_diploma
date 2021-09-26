# -*- coding: utf-8 -*-
# Telegram-бот для поиска отелей на сайте Hotels.com

import telebot
from pony.orm import db_session
from datetime import datetime
from settings import TOKEN
import handlers
from intents import INTENTS, SCENARIOS, HELP_ANSWER
from models import SearchHistory

bot = telebot.TeleBot(TOKEN)

users_state = {}
# словарь из словарей вида {user_id: {'scenario_name': 'lowerprice',
#                                     'step_name': 'step2',
#                                     'context': {'city': 'paris', 'numbers': '3', ..., ...}
#                                     }
#                           },
# для временного хранения состояний сценариев пользователей. При старте сценария создается элемент
# словаря с ключом user_id, при завершении сценария элемент удаляется.


@bot.message_handler(content_types=['text'])
@db_session
def on_event(message) -> None:
    """
    начинает или продолжает сценарий, или просто выдаёт сообщение в ответ на сообщение от пользователя
    :param message: Message object, включающий в т.ч. идентификатор пользователя и текст сообщения
    :return:
    """
    text = message.text.lower()
    user_id = message.from_user.id
    state = users_state.get(user_id)

    for intent in INTENTS:
        if text == intent['command']:
            # если сообщение является командой из перечня допустимых команд
            # прекращение текущего сценария
            finish_scenario(user_id)
            if intent['answer']:
                # если действие по команде - просто выдача ответного сообщения
                bot.send_message(message.from_user.id, intent['answer'])
            else:
                # начало нового сценария
                scenario_name = intent['scenario']
                start_scenario(user_id, scenario_name)
            break
    else:
        if state is not None:
            # продолжение начатого сценария
            continue_scenario(user_id, state, text)
        else:
            # выдача ответного сообщения на недопустимую команду
            bot.send_message(message.from_user.id, HELP_ANSWER)


def start_scenario(user_id: int, scenario_name: str) -> None:
    """
    начинает выполнение нового сценария
    :param user_id: идентификатор пользователя
    :param scenario_name: название сценария
    :return:
    """
    scenario = SCENARIOS[scenario_name]
    first_step = scenario['first_step']
    step = scenario['steps'][first_step]
    users_state[user_id] = {'scenario_name': scenario_name, 'step_name': first_step, 'context': {}}
    bot.send_message(user_id, step['text'])


def continue_scenario(user_id: int, state: dict, text: str) -> None:
    """
    продолжает выполнение сценария
    :param user_id: идентификатор пользователя
    :param state: словарь, содержащий состояние сценария пользователя
    :param text: текст сообщения
    :return:
    """
    steps = SCENARIOS[state['scenario_name']]['steps']
    step = steps[state['step_name']]
    handler = getattr(handlers, step['handler'])
    if handler(text=text, context=state['context'], scenario_name=state['scenario_name'], user_id=user_id):
        # при успешной отработке шага выдача сообщения следующего шага сценария
        next_step = steps[step['next_step']]
        bot.send_message(user_id, next_step['text'].format(**state['context']))
        if next_step['next_step']:
            # если есть следующий шаг, то переход на него
            state['step_name'] = step['next_step']
        else:
            # иначе завершение сценария
            if state['scenario_name'] != 'history':
                # сохранение запроса в БД для команд поиска отелей
                search_date_time = datetime.now().strftime('%d.%m.%Y %H:%M')
                SearchHistory(user_id=user_id, search_date=search_date_time,
                              command=state['scenario_name'], hotels=state['context']['hotels'])
            finish_scenario(user_id)
    else:
        # при неудачной обработке шага - сообщение об ошибке и повтор этого шага
        bot.send_message(user_id, step['failure_text'])


def finish_scenario(user_id: int) -> None:
    """
    завершает сценарий
    :param user_id: идентификатор пользователя
    :return:
    """
    users_state.pop(user_id, 0)


if __name__ == '__main__':
    bot.polling()
