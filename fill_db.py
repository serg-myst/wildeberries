from sqlalchemy import insert, select, func
from database import session_maker
from models import delivery_type, exchange, currency, order_item
from save_data import save_data
from save_data import session as save_data_session
from sys import argv
import json
from pydantic import ValidationError
from schemas import OrderItem
from config import CURRENCIES

session = session_maker()


def fill_delivery():
    query = select(func.count()).select_from(delivery_type)
    res = session.execute(query).scalar()
    values_list = [{'id': 1, 'enum': 'dbs', 'name': 'Доставка на склад Wildberries'},
                   {'id': 2, 'enum': 'fbs', 'name': 'Доставка силами продавца'}, ]
    if res == 0:
        query = insert(delivery_type).values(values_list)
        session.execute(query)
        session.commit()


def fill_exchange():
    query = select(func.count()).select_from(exchange)
    res = session.execute(query).scalar()
    values_list = [{'is_started': 0}, ]
    if res == 0:
        query = insert(exchange).values(values_list)
        session.execute(query)
        session.commit()


def fill_currency():
    for item in CURRENCIES:
        save_data(item, currency, ['code'])
    save_data_session.commit()


def fill_order_item_test():
    with open('test.json', 'r', encoding='utf-8') as f:
        for data in json.load(f)['orders']:
            try:
                order_row = OrderItem(**data)
            except ValidationError as err:
                print(f'Данные не прошли по схеме. {err.json()}')
            else:
                save_data(order_row.dict(), order_item, ['orderId', 'nmId'])
        save_data_session.commit()


if __name__ == '__main__':
    if len(argv) > 1:
        script, type_query = argv
        if type_query == 'd':
            fill_delivery()
        if type_query == 'e':
            fill_exchange()
        if type_query == 'c':
            fill_currency()
