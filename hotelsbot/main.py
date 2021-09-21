import telebot
from pony.orm import db_session
from settings import TOKEN
from models import UserState
# from hotelsbot import handlers
import handlers
from intents import INTENTS, SCENARIOS, HELP_ANSWER

bot = telebot.TeleBot(TOKEN)

# users_state = {}
# словарь вида {user_id: {'scenario_name': 'lowerprice',
#                        'step_name': 'step2',
#                        'context': {'city': 'paris', 'numbers': 3, ..., ...}
#                        }
#              }


@bot.message_handler(content_types=['text'])
@db_session
def on_event(message):
    text = message.text.lower()
    user_id = message.from_user.id
    # state = users_state.get(user_id)
    state = UserState.get(user_id=str(user_id))

    for intent in INTENTS:
        if text == intent['command']:
            if intent['answer']:
                # finish_scenario(user_id)
                finish_scenario(state)
                bot.send_message(message.from_user.id, intent['answer'])
            else:
                # finish_scenario(user_id)
                finish_scenario(state)
                scenario_name = intent['scenario']
                start_scenario(user_id, scenario_name)
            break
    else:
        if state is not None:
            continue_scenario(user_id, state, text)
        else:
            bot.send_message(message.from_user.id, HELP_ANSWER)


def start_scenario(user_id, scenario_name):
    scenario = SCENARIOS[scenario_name]
    first_step = scenario['first_step']
    step = scenario['steps'][first_step]
    # users_state[user_id] = {'scenario_name': scenario_name, 'step_name': first_step, 'context': {}}
    UserState(user_id=str(user_id), scenario_name=scenario_name, step_name=first_step, context={})
    bot.send_message(user_id, step['text'])


def continue_scenario(user_id, state, text):
    # steps = SCENARIOS[state['scenario_name']]['steps']
    steps = SCENARIOS[state.scenario_name]['steps']
    #  continue scenario
    # step = steps[state['step_name']]
    step = steps[state.step_name]
    handler = getattr(handlers, step['handler'])
    # if handler(text=text, context=state['context'], scenario_name=state['scenario_name']):
    if handler(text=text, context=state.context, scenario_name=state.scenario_name):
        # next_step
        next_step = steps[step['next_step']]
        # bot.send_message(user_id, next_step['text'].format(**state['context']))
        bot.send_message(user_id, next_step['text'].format(**state.context))
        if next_step['next_step']:
            # switch to next step
            # state['step_name'] = step['next_step']
            state.step_name = step['next_step']
        else:
            # pprint(users_state)
            # finish_scenario(user_id)
            finish_scenario(state)
            # pprint(users_state)

    else:
        # retry current step
        bot.send_message(user_id, step['failure_text'])


def finish_scenario(state):
    # users_state.pop(user_id, 0)
    if state is not None:
        state.delete()


if __name__ == '__main__':
    bot.polling()
