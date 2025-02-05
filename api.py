from config import TOKEN, PRICES_URL, WAREHOUSES_URL, OFFICES_URL, GOODS_URL, GOODS_QUERY, ORDERS_URL, ORDERS_ALL_URL
import requests
from requests.exceptions import ConnectionError as ConnectionErrorRequests
from requests.exceptions import InvalidSchema
import json
from config import LOGGER as log
from datetime import datetime
from save_data import save_error


def headers():
    return {'Authorization': TOKEN}


def get_orders_by_date_api():
    try:
        date_to_query = int(
            datetime.fromisoformat(
                str(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))).timestamp())
        parameters = {'limit': 1000, 'next': 0, 'dateFrom': date_to_query}
        response = requests.get(ORDERS_ALL_URL, headers=headers(), params=parameters)
        if response.status_code != 200:
            content = json.loads(response.content)
            err_txt = (f'Ошибка получения данных по всем заказам за день. Статус ответа {response.status_code}.'
                       f' Текст ответа {content.statusText}')
            save_error(err_txt)
            log.error(err_txt)
            raise ConnectionErrorRequests
        content = json.loads(response.content)
        log.info(f'Получены данные о всем заказам за день с {ORDERS_ALL_URL}')
        return content.get('orders')
    except ConnectionError as e:
        err_txt = f'Ошибка ConnectionError. Данные не получены {ORDERS_ALL_URL}. Ошибка: {e}'
        save_error(err_txt)
        log.exception(err_txt)


def get_office_api():
    try:
        response = requests.get(OFFICES_URL, headers=headers())
        if response.status_code != 200:
            err_txt = f'Ошибка получения данных по торговым площадкам. Статус ответа {response.status_code}'
            save_error(err_txt)
            log.error(err_txt)
            raise ConnectionErrorRequests
        content = json.loads(response.content)
        log.info(f'Получены данные по торговым площадкам с {OFFICES_URL}')
        return content
    except ConnectionError as e:
        err_txt = f'Ошибка ConnectionError. Данные не получены {OFFICES_URL}. Ошибка: {e}'
        save_error(err_txt)
        log.exception(err_txt)


def get_warehouse_api():
    try:
        response = requests.get(WAREHOUSES_URL, headers=headers())
        if response.status_code != 200:
            err_txt = f'Ошибка получения данных по складам продавца. Статус ответа {response.status_code}'
            save_error(err_txt)
            log.error(err_txt)
            raise ConnectionErrorRequests
        content = json.loads(response.content)
        log.info(f'Получены данные по складам продавца с {WAREHOUSES_URL}')
        return content
    except ConnectionError as e:
        err_txt = f'Ошибка ConnectionError. Данные не получены {WAREHOUSES_URL}. Ошибка: {e}'
        save_error(err_txt)
        log.exception(err_txt)


def get_price_api():
    try:
        response = requests.get(PRICES_URL, headers=headers())
        if response.status_code != 200:
            err_txt = f'Ошибка получения данных по ценам. Статус ответа {response.status_code}'
            save_error(err_txt)
            log.error(err_txt)
            raise ConnectionErrorRequests
        content = json.loads(response.content)
        log.info(f'Получены данные по ценам с {PRICES_URL}')
        return content
    except ConnectionError as e:
        err_txt = f'Ошибка ConnectionError. Данные не получены {PRICES_URL}. Ошибка: {e}'
        save_error(err_txt)
        log.exception(err_txt)


def get_goods_api():
    try:
        response = requests.post(GOODS_URL, json=GOODS_QUERY, headers=headers())
        if response.status_code != 200:
            log.error(f'Ошибка получения данных по товарам. Статус ответа {response.status_code}')
            raise ConnectionErrorRequests
        content = json.loads(response.content)
        content_data = content.get('cards')
        if content_data is None:
            err_txt = (f'Ошибка получения данных по товарам. Ошибка разбора полученного файла.'
                       f' Нет ключа: get("data").get("cards")')
            save_error(err_txt)
            log.error(err_txt)
            raise InvalidSchema
        log.info(f'Получены данные по товарам с {GOODS_URL}')
        return content_data
    except ConnectionError as e:
        err_txt = f'Ошибка ConnectionError. Данные не получены {GOODS_URL}. Ошибка: {e}'
        save_error(err_txt)
        log.exception(err_txt)


def get_orders_api():
    try:
        response = requests.get(ORDERS_URL, headers=headers())
        if response.status_code != 200:
            err_txt = f'Ошибка получения данных по новым заказам. Статус ответа {response.status_code}'
            save_error(err_txt)
            log.error(err_txt)
            raise ConnectionErrorRequests
        content = json.loads(response.content)
        log.info(f'Получены данные по новым заказам с {ORDERS_URL}')
        return content.get('orders')
    except ConnectionError as e:
        err_txt = f'Ошибка ConnectionError. Данные не получены {ORDERS_URL}. Ошибка: {e}'
        save_error(err_txt)
        log.exception()


if __name__ == '__main__':
    pass
