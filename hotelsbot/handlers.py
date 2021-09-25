# -*- coding: utf-8 -*-
from pony.orm import select
from rapidapi_utils import get_city, get_hotels
from models import SearchHistory

MAX_REQUESTS_ITEMS = 25
MIN_DISTANCE = 1
MAX_DISTANCE = 9


def handle_city(text: str, context: dict, scenario_name: str, user_id: int) -> bool:
    """
    Обрабатывает названия города.
    Если город найден, заносит его id в context.
    :param text: текст сообщения пользователя
    :param context: словарь с информацией, получаемой из ответов пользователя
    :param scenario_name: название сценария
    :param user_id: идентификатор пользователя
    :return:
    """
    # получения id города по названию
    city_id = get_city(text)
    if city_id:
        context['city'] = city_id
        return True
    else:
        return False


def handle_numbers(text: str, context: dict, scenario_name: str, user_id: int) -> bool:
    """
    Обрабатывает количества выводимых отелей, затем запрашивает выдачу финального результата.
    При корректном значении  сначала заносит в context количество, а затем - финальный результат всего запроса.
    :param text: текст сообщения пользователя
    :param context: словарь с информацией, получаемой из ответов пользователя
    :param scenario_name: название сценария
    :param user_id: идентификатор пользователя
    :return:
    """
    if text.isdigit() and int(text) <= MAX_REQUESTS_ITEMS:
        context['numbers'] = text
        # запрос финального результата всего запроса
        context['hotels'] = get_hotels(context, scenario_name)
        return True
    else:
        return False


def handle_min_price(text: str, context: dict, scenario_name: str, user_id: int) -> bool:
    """
    Обрабатывает минимальную цену.
    При корректном значении  заносит её в context.
    :param text: текст сообщения пользователя
    :param context: словарь с информацией, получаемой из ответов пользователя
    :param scenario_name: название сценария
    :param user_id: идентификатор пользователя
    :return:
    """
    if text.isdigit():
        context['min_price'] = text
        return True
    else:
        return False


def handle_max_price(text: str, context: dict, scenario_name: str, user_id: int) -> bool:
    """
    Обрабатывает максимальную цену.
    При корректном значении  заносит её в context.
    :param text: текст сообщения пользователя
    :param context: словарь с информацией, получаемой из ответов пользователя
    :param scenario_name: название сценария
    :param user_id: идентификатор пользователя
    :return:
    """
    if text.isdigit() and int(text) > int(context['min_price']):
        context['max_price'] = text
        return True
    else:
        return False


def handle_distance(text: str, context: dict, scenario_name: str, user_id: int) -> bool:
    """
    Обрабатывает максимальную дистанцию.
    При корректном значении  заносит её в context.
    :param text: текст сообщения пользователя
    :param context: словарь с информацией, получаемой из ответов пользователя
    :param scenario_name: название сценария
    :param user_id: идентификатор пользователя
    :return:
    """
    if text.isdigit() and MIN_DISTANCE <= int(text) <= MAX_DISTANCE:
        context['max_distance'] = text
        return True
    else:
        return False


def handle_history(text: str, context: dict, scenario_name: str, user_id: int) -> bool:
    """
        Запрашивает подтверждение на вывод истории запросов.
        В случае подтверждения получает историю запросов пользователя и заносит её в context.
        :param text: текст сообщения пользователя
        :param context: словарь с информацией, получаемой из ответов пользователя
        :param scenario_name: название сценария
        :param user_id: идентификатор пользователя
        :return:
        """
    if text in ['да', 'нет']:
        if text == 'да':
            context['history'] = user_search_history(user_id)
        else:
            context['history'] = 'Вы отказались выводить историю ваших запросов'
        return True
    else:
        return False


def user_search_history(user_id: int) -> str:
    """
    Получает из таблицы БД SearchHistory всю историю поиска отелей для пользователя по uer_id.
    Возвращает сформированную строку с историей. Если нет истории поиска - соответствующее сообщение.
    :param user_id: идентификатор пользователя
    :return history: история поиска
    """
    search = select(s for s in SearchHistory if user_id == s.user_id)
    if search:
        history_list = []
        for search_item in search:
            search_item_line = f'{25*"*"}\nдата и время поиска:{search_item.search_date}\n' \
                               f'тип поиска:{search_item.command}\nрезультат поиска:\n{search_item.hotels}\n'
            history_list.append(search_item_line)
        history = '\n'.join(history_list)
    else:
        history = 'Вы пока не делали запросов на поиск отелей'
    return history
