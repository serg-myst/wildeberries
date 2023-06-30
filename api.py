from config import TOKEN, PRICES_URL, WAREHOUSES_URL, OFFICES_URL, GOODS_URL, GOODS_QUERY
import requests
import json


def headers():
    return {'Authorization': TOKEN}


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
    # get_price_api()
    # get_goods_api()
