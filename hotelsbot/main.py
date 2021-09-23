# -*- coding: utf-8 -*-
import telebot
from pony.orm import db_session
from settings import TOKEN
from models import UserState
import handlers
from intents import INTENTS, SCENARIOS, HELP_ANSWER

bot = telebot.TeleBot(TOKEN)


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
    state = UserState.get(user_id=str(user_id))

    for intent in INTENTS:
        if text == intent['command']:
            # если сообщение является командой из перечня допустимых команд
            if intent['answer']:
                # если действие по команде - просто выдача ответного сообщения
                finish_scenario(state)
                bot.send_message(message.from_user.id, intent['answer'])
            else:
                # начало нового сценария
                finish_scenario(state)
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


def start_scenario(user_id: str, scenario_name: str) -> None:
    """
    начинает выполнение нового сценария
    :param user_id: идентификатор пользователя
    :param scenario_name: название сценария
    :return:
    """
    scenario = SCENARIOS[scenario_name]
    first_step = scenario['first_step']
    step = scenario['steps'][first_step]
    UserState(user_id=str(user_id), scenario_name=scenario_name, step_name=first_step, context={})
    bot.send_message(user_id, step['text'])


def continue_scenario(user_id: str, state: UserState, text: str) -> None:
    """
    продолжает выполнение сценария
    :param user_id: идентификатор пользователя
    :param state: UserState object, содержащий состояние сценария
    :param text: текст сообщения
    :return:
    """
    steps = SCENARIOS[state.scenario_name]['steps']
    step = steps[state.step_name]
    handler = getattr(handlers, step['handler'])
    if handler(text=text, context=state.context, scenario_name=state.scenario_name):
        # при успешной отработке шага выдача сообщения следующего шага сценария
        next_step = steps[step['next_step']]
        bot.send_message(user_id, next_step['text'].format(**state.context))
        if next_step['next_step']:
            # если есть следующий шаг, то переход на него
            state.step_name = step['next_step']
        else:
            # иначе завершение сценария
            finish_scenario(state)
    else:
        # при неудачной обработке шага - сообщение об ошибке и повтор этого шага
        bot.send_message(user_id, step['failure_text'])


def finish_scenario(state: UserState) -> None:
    """
    завершает сценарий
    :param state: UserState object, содержащий состояние сценария
    :return:
    """
    if state is not None:
        state.delete()


if __name__ == '__main__':
    bot.polling()
