import telebot
from settings import TOKEN
from handlers import continue_scenario, start_scenario, finish_scenario
from intents import INTENTS, HELP_ANSWER

bot = telebot.TeleBot(TOKEN)

users_state = {}
# словарь вида user_id: {'scenario_name': 'lowerprice',
#                        'step_name': 'step2',
#                        'context': {'city': 'paris', 'numbers': 3}
#                        }


@bot.message_handler(content_types=['text'])
def on_event(message):
    text = message.text.lower()
    user_id = message.from_user.id
    state = users_state.get(user_id)
    print(f'пришло сообщение {text} от пользователя {user_id}')

    for intent in INTENTS:
        if text == intent['command']:
            if intent['answer']:
                finish_scenario(user_id)
                bot.send_message(message.from_user.id, intent['answer'])
            else:
                finish_scenario(user_id)
                scenario_name = intent['scenario']
                start_scenario(user_id, scenario_name, text)
                bot.send_message(message.from_user.id, f'тест - начинаем сценарий: {scenario_name}')
            break
    else:
        if state is not None:
            continue_scenario(user_id, state, text)
        else:
            bot.send_message(message.from_user.id, HELP_ANSWER)


if __name__ == '__main__':
    bot.polling()
