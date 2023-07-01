from config import TOKEN, PRICES_URL, WAREHOUSES_URL, OFFICES_URL, GOODS_URL, GOODS_QUERY, FILE_LOG
import requests
import json
import time
from config import LOGGER as log


def headers():
    return {'Authorization': TOKEN}


def get_office_api():
    while True:
        try:
            response = requests.get(OFFICES_URL, headers=headers())
            if response.status_code != 200:
                log.error(f'Ошибка получения данных по площадкам. Статус ответа {response.status_code}')
                return []
            content = json.loads(response.content)
            log.info(f'Получен данные с {OFFICES_URL}')
            return content
        except ConnectionError:
            log.exception(f'Ошибка ConnectionError. Данные не получены {OFFICES_URL}')
            time.sleep(1)


def get_warehouse_api():
    response = requests.get(WAREHOUSES_URL, headers=headers())
    if response.status_code != 200:
        print(f'Ошибка получения данных по складам. Статус ответа {response.status_code}')
        return []
    content = json.loads(response.content)
    return content


def get_price_api():
    response = requests.get(PRICES_URL, headers=headers())
    if response.status_code != 200:
        print(f'Ошибка получения данных по ценам. Статус ответа {response.status_code}')
        return []
    content = json.loads(response.content)
    return content


def get_goods_api():
    response = requests.post(GOODS_URL, json=GOODS_QUERY, headers=headers())
    if response.status_code != 200:
        print(f'Ошибка получения данных по товарам. Статус ответа {response.status_code}')
        # Записать в логи ошибку
        return []
    try:
        content = json.loads(response.content)
        return content.get('data').get('cards')
    except AttributeError as e:
        # Записать в логи ошибку
        return []


if __name__ == '__main__':
    pass
