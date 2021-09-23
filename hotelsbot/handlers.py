# -*- coding: utf-8 -*-
from rapidapi_utils import get_city, get_hotels

MAX_REQUESTS_ITEMS = 25
MIN_DISTANCE = 1
MAX_DISTANCE = 9


def handle_city(text: str, context: dict, scenario_name: str) -> bool:
    """
    Обрабатывает названия города.
    Если город найден, заносит его id в context.
    :param text: текст сообщения пользователя
    :param context: словарь с информацией, получаемой из ответов пользователя
    :param scenario_name: название сценария
    :return:
    """
    # получения id города по названию
    city_id = get_city(text)
    if city_id:
        context['city'] = city_id
        return True
    else:
        return False


def handle_numbers(text: str, context: dict, scenario_name: str) -> bool:
    """
    Обрабатывает количества выводимых отелей, затем запрашивает выдачу финального результата.
    При корректном значении  сначала заносит в context количество, а затем - финальный результат всего запроса.
    :param text: текст сообщения пользователя
    :param context: словарь с информацией, получаемой из ответов пользователя
    :param scenario_name: название сценария
    :return:
    """
    if text.isdigit() and int(text) <= MAX_REQUESTS_ITEMS:
        context['numbers'] = text
        # запрос финального результата всего запроса
        context['hotels'] = get_hotels(context, scenario_name)
        return True
    else:
        return False


def handle_min_price(text: str, context: dict, scenario_name: str) -> bool:
    """
        Обрабатывает минимальную цену.
        При корректном значении  заносит её в context.
        :param text: текст сообщения пользователя
        :param context: словарь с информацией, получаемой из ответов пользователя
        :param scenario_name: название сценария
        :return:
        """
    if text.isdigit():
        context['min_price'] = text
        return True
    else:
        return False


def handle_max_price(text: str, context: dict, scenario_name: str) -> bool:
    """
            Обрабатывает максимальную цену.
            При корректном значении  заносит её в context.
            :param text: текст сообщения пользователя
            :param context: словарь с информацией, получаемой из ответов пользователя
            :param scenario_name: название сценария
            :return:
            """
    if text.isdigit() and int(text) > int(context['min_price']):
        context['max_price'] = text
        return True
    else:
        return False


def handle_distance(text: str, context: dict, scenario_name: str) -> bool:
    """
            Обрабатывает максимальную дистанцию.
            При корректном значении  заносит её в context.
            :param text: текст сообщения пользователя
            :param context: словарь с информацией, получаемой из ответов пользователя
            :param scenario_name: название сценария
            :return:
            """
    if text.isdigit() and MIN_DISTANCE <= int(text) <= MAX_DISTANCE:
        context['max_distance'] = text
        return True
    else:
        return False
