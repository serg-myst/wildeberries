from config import TOKEN, PRICES_URL, WAREHOUSES_URL, OFFICES_URL, GOODS_URL, GOODS_QUERY, ORDERS_URL
import requests
from requests.exceptions import ConnectionError as ConnectionErrorRequests
from requests.exceptions import InvalidSchema
import json
from config import LOGGER as log


def headers():
    return {'Authorization': TOKEN}


def get_office_api():
    try:
        response = requests.get(OFFICES_URL, headers=headers())
        if response.status_code != 200:
            log.error(f'Ошибка получения данных по торговым площадкам. Статус ответа {response.status_code}')
            raise ConnectionErrorRequests
        content = json.loads(response.content)
        log.info(f'Получены данные по торговым площадкам с {OFFICES_URL}')
        return content
    except ConnectionError as e:
        log.exception(f'Ошибка ConnectionError. Данные не получены {OFFICES_URL}. Ошибка: {e}')


def get_warehouse_api():
    try:
        response = requests.get(WAREHOUSES_URL, headers=headers())
        if response.status_code != 200:
            log.error(f'Ошибка получения данных по складам продавца. Статус ответа {response.status_code}')
            raise ConnectionErrorRequests
        content = json.loads(response.content)
        log.info(f'Получены данные по складам продавца с {WAREHOUSES_URL}')
        return content
    except ConnectionError as e:
        log.exception(f'Ошибка ConnectionError. Данные не получены {WAREHOUSES_URL}. Ошибка: {e}')


def get_price_api():
    try:
        response = requests.get(PRICES_URL, headers=headers())
        if response.status_code != 200:
            log.error(f'Ошибка получения данных по ценам. Статус ответа {response.status_code}')
            raise ConnectionErrorRequests
        content = json.loads(response.content)
        log.info(f'Получены данные по ценам с {PRICES_URL}')
        return content
    except ConnectionError as e:
        log.exception(f'Ошибка ConnectionError. Данные не получены {PRICES_URL}. Ошибка: {e}')


def get_goods_api():
    try:
        response = requests.post(GOODS_URL, json=GOODS_QUERY, headers=headers())
        if response.status_code != 200:
            log.error(f'Ошибка получения данных по товарам. Статус ответа {response.status_code}')
            raise ConnectionErrorRequests
        content = json.loads(response.content)
        content_data = content.get('data').get('cards')
        if content_data is None:
            log.error(
                f'Ошибка получения данных по товарам. Ошибка разбора полученного файла.'
                f' Нет ключа: get("data").get("cards")')
            raise InvalidSchema
        log.info(f'Получены данные по товарам с {GOODS_URL}')
        return content_data
    except ConnectionError as e:
        log.exception(f'Ошибка ConnectionError. Данные не получены {GOODS_URL}. Ошибка: {e}')


def get_orders_api():
    try:
        response = requests.get(ORDERS_URL, headers=headers())
        if response.status_code != 200:
            log.error(f'Ошибка получения данных по новым заказам. Статус ответа {response.status_code}')
            raise ConnectionErrorRequests
        content = json.loads(response.content)
        log.info(f'Получены данные по новым заказам с {ORDERS_URL}')
        return content.get('orders')
    except ConnectionError as e:
        log.exception(f'Ошибка ConnectionError. Данные не получены {ORDERS_URL}. Ошибка: {e}')


if __name__ == '__main__':
    pass
