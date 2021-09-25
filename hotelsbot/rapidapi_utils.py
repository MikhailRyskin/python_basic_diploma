# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime, timedelta
from settings import RAPIDAPI_KEY

DAY_TOMORROW = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
DAY_AFTER_TOMORROW = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')
NOT_HOTELS_MESSAGE = 'Мы не нашли отелей по вашему запросу. Попробуйте другой вариант запроса.'


def get_city(text: str) -> str:
    """
    Ищет город по названию в locations.
    При успешном поиске возвращает id города. Если город не найден,  возвращает пустую строку.
    :param text: название города, введённое пользователем
    :return destination_id: id города
    """
    url = "https://hotels4.p.rapidapi.com/locations/search"
    querystring = {"query": text, "locale": "ru_RU"}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    result_locations_search = json.loads(response.text)
    destination_id = ''
    for group in result_locations_search['suggestions']:
        if group['group'] == 'CITY_GROUP':
            if group['entities']:
                destination_id = group['entities'][0]['destinationId']
                break
    return destination_id


def get_hotels(context: dict, scenario_name: str) -> str:
    """
    Формирует финальный список отелей на основе всего запроса пользователя.
    Возвращает строку с подробной информацией о всех отелях. Если нет отелей, соответствующих запросу,
    возвращает пустую строку.
    :param context: словарь с информацией, получаемой из ответов пользователя
    :param scenario_name: название сценария
    :return hotels_line: информация о найденных отелях
    """
    url = "https://hotels4.p.rapidapi.com/properties/list"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }

    page_number = '1'
    next_page = True
    hotels_list = []
    pages_count = 0
    # запрос нескольких страниц, если требуется
    while next_page and pages_count < 5:
        pages_count += 1
        querystring = {"destinationId": context['city'], "pageNumber": page_number, "pageSize": context['numbers'],
                       "checkIn": DAY_TOMORROW, "checkOut": DAY_AFTER_TOMORROW, "adults1": "1",
                       "sortOrder": "PRICE", "locale": "ru_RU", "currency": "USD"}
        # корректировка querystring запроса в зависимости от сценария
        if scenario_name == 'highprice':
            querystring['sortOrder'] = 'PRICE_HIGHEST_FIRST'
        if scenario_name == 'bestdeal':
            querystring['pageSize'] = '25'
            querystring['sortOrder'] = 'DISTANCE_FROM_LANDMARK'
            querystring['landmarkIds'] = 'City center'
            querystring['priceMin'] = context['min_price']
            querystring['priceMax'] = context['max_price']

        response = requests.request("GET", url, headers=headers, params=querystring)
        response_properties_list = json.loads(response.text)
        # различные обработки результата запроса в зависимости от сценария
        if scenario_name == 'lowprice' or scenario_name == 'highprice':
            hotels_list = response_properties_list['data']['body']['searchResults']['results']
            next_page = False
        elif scenario_name == 'bestdeal':
            page_search_results = response_properties_list['data']['body']['searchResults']
            page_results = page_search_results['results']
            for hotel_item in page_results:
                # поиск в результате запроса отелей, соответствующих дополнительному требованию по дистанции
                distance = hotel_item['landmarks'][0]['distance']
                # преобразование строки вида '1,7 км' в число
                distance_from_center = float('.'.join(distance[:-3].split(',')))
                if distance_from_center <= int(context['max_distance']):
                    hotels_list.append(hotel_item)
                if len(hotels_list) == int(context['numbers']):
                    # если найдено необходимое число отелей - прекращение поиска
                    next_page = False
                    break
            if next_page:
                # получение следующей страницы для запроса, если это необходимо (если она есть)
                if 'pagination' in page_search_results and 'nextPageNumber' in page_search_results['pagination']:
                    page_number = str(page_search_results['pagination']['nextPageNumber'])
                    next_page = True
                else:
                    next_page = False
        else:
            next_page = False
    # формирование строки, содержащей название, адрес, цену и расстояние до центра для каждого отеля
    # из списка, сформированного по запросу пользователя. Если по запросу не было найдено отелей,
    # строка содержит сообщение об этом
    if hotels_list:
        hotels = []
        for hotel in hotels_list:
            name = hotel['name']
            address_dict = hotel['address']
            address = address_dict.get('locality', 'не указан ') + ', ' + address_dict.get('streetAddress',
                                                                                           'адрес не указан')
            if 'ratePlan' in hotel:
                price = hotel['ratePlan']['price']['current']
            else:
                price = 'не указана'
            distance_from_center = hotel['landmarks'][0]['distance']
            hotel_line = f'{name}, адрес:{address}, расстояние от центра:{distance_from_center}, цена:{price}\n'
            hotels.append(hotel_line)
        hotels_line = '\n'.join(hotels)
    else:
        hotels_line = NOT_HOTELS_MESSAGE
    return hotels_line
