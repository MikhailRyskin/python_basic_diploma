import requests
import json
from datetime import datetime, timedelta
from settings import RAPIDAPI_KEY

DAY_TOMORROW = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
DAY_AFTER_TOMORROW = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')
MAX_REQUESTS_ITEMS = 25


def handle_city(text, context, scenario_name):
    city_id = get_city(text)
    if city_id:
        context['city'] = city_id
        return True
    else:
        return False


def get_city(text):
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


def handle_numbers(text, context, scenario_name):
    if text.isdigit() and int(text) <= MAX_REQUESTS_ITEMS:
        context['numbers'] = text
        context['hotels'] = get_hotels(context, scenario_name)
        return True
    else:
        return False


def get_hotels(context, scenario_name):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    querystring = {"destinationId": context['city'], "pageNumber": "1", "pageSize": context['numbers'],
                   "checkIn": DAY_TOMORROW, "checkOut": DAY_AFTER_TOMORROW, "adults1": "1",
                   "sortOrder": "PRICE", "locale": "ru_RU", "currency": "USD"}
    if scenario_name == 'highprice':
        querystring['sortOrder'] = 'PRICE_HIGHEST_FIRST'

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_properties_list = json.loads(response.text)

    hotels_list = response_properties_list['data']['body']['searchResults']['results']
    hotels = []
    hotels_line = ''
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
        hotel_line = f'{name}, адрес:{address}, расстояние от центра:{distance_from_center}, цена:{price}'
        hotels.append(hotel_line)
        hotels_line = '\n'.join(hotels)
    return hotels_line


def handle_price(text, context, scenario_name):
    return True


def handle_distance(text, context, scenario_name):
    return True
