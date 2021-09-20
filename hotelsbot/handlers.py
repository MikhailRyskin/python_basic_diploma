from rapidapi_utils import get_city, get_hotels

MAX_REQUESTS_ITEMS = 25
MIN_DISTANCE = 1
MAX_DISTANCE = 9


def handle_city(text, context, scenario_name):
    city_id = get_city(text)
    if city_id:
        context['city'] = city_id
        return True
    else:
        return False


def handle_numbers(text, context, scenario_name):
    if text.isdigit() and int(text) <= MAX_REQUESTS_ITEMS:
        context['numbers'] = text
        context['hotels'] = get_hotels(context, scenario_name)
        return True
    else:
        return False


def handle_min_price(text, context, scenario_name):
    if text.isdigit():
        context['min_price'] = text
        return True
    else:
        return False


def handle_max_price(text, context, scenario_name):
    if text.isdigit() and int(text) > int(context['min_price']):
        context['max_price'] = text
        return True
    else:
        return False


def handle_distance(text, context, scenario_name):
    if text.isdigit() and MIN_DISTANCE <= int(text) <= MAX_DISTANCE:
        context['max_distance'] = text
        return True
    else:
        return False
