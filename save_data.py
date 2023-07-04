from pydantic import ValidationError
from database import session_maker
from sqlalchemy import insert, select, func
from config import LOGGER as log
from models import delivery_type, order, order_item, new_order
from sqlalchemy.dialects.sqlite import insert
from schemas import Order, OrderItem, NewOrder

import json

session = session_maker()


def save_data(item, table, id):
    insert_stmt = insert(table).values(item)
    do_update_stmt = insert_stmt.on_conflict_do_update(
        index_elements=id,
        set_=item)
    session.execute(do_update_stmt)


def get_wb_data(table, model, method, id=None):
    if id is None:
        id = ['id']
    data_list = method()
    for data in data_list:
        try:
            item = model(**data)
        except ValidationError as err:
            log.error(f'Данные не прошли по схеме. {err.json()}')
        else:
            save_data(item.dict(), table, id)
    try:
        session.commit()
    except SystemError as e:
        log.error(f'Ошибка записи данных по {table}. {e}')


def fill_delivery():
    query = select(func.count()).select_from(delivery_type)
    res = session.execute(query).scalar()
    values_list = [{'id': 1, 'enum': 'dbs', 'name': 'Доставка на склад Wildberries'},
                   {'id': 2, 'enum': 'fbs', 'name': 'Доставка силами продавца'}, ]
    if res == 0:
        query = insert(delivery_type).values(values_list)
        session.execute(query)
        session.commit()


def get_wb_order(method):
    data_list = method()
    for data in data_list:
        try:
            item_head = Order(**data)
            order_row = OrderItem(**data)
            order_send = NewOrder(**data)
        except ValidationError as err:
            print(err.json())
        else:
            save_data(item_head.dict(), order, ['id'])
            save_data(order_row.dict(), order_item, ['orderId', 'nmId'])
            save_data(order_send.dict(), new_order, ['orderId'])
    session.commit()


# ТЕСТИРОВАНИЕ. УБРАТЬ!!!
def save(item):
    print(item)
    insert_stmt = insert(order).values(item)
    do_update_stmt = insert_stmt.on_conflict_do_update(
        index_elements=['id'],
        set_=item)
    session.execute(do_update_stmt)


def save_order_row(item):
    print(item)
    insert_stmt = insert(order_item).values(item)
    do_update_stmt = insert_stmt.on_conflict_do_update(
        index_elements=['orderId', 'nmId'],
        set_=item)
    session.execute(do_update_stmt)


def get_wb_order_test():
    file_name = 'response_1688373087780_new.json'
    item_list = []
    with open(file_name, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
        for data in data_list.get('orders'):
            try:
                item_head = Order(**data)
                order_row = OrderItem(**data)
            except ValidationError as err:
                print(err.json())
            else:
                save(item_head.dict())
                save_order_row(order_row.dict())
        session.commit()

# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-on-conflict-insert
