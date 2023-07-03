from pydantic import ValidationError
from database import session_maker
from sqlalchemy import insert, delete, select, update, func
from config import LOGGER as log
from models import delivery_type, order, order_item
from sqlalchemy.dialects.sqlite import insert

session = session_maker()

import json
from schemas import Order, OrderItem

query_1 = ''


def save_data(item_list, table):
    # Данных у нас совсем мало. Сначала все удалим и добавим новые данные
    try:
        query = delete(table)
        session.execute(query)
        session.commit()

        query = insert(table).values(item_list)
        session.execute(query)
        session.commit()
        log.info(f'Записаны данные по {table}')
    except SystemError as e:
        log.error(f'Ошибка записи данных по {table}. {e}')
        raise e


def get_wb_data(table, model, method):
    data_list = method()
    item_list = []
    for data in data_list:
        try:
            item = model(**data)
        except ValidationError as err:
            log.error(f'Данные не прошли по схеме. {err.json()}')
        else:
            item_list.append(item.dict())
    if len(item_list) > 0:
        save_data(item_list, table)


def fill_delivery():
    query = select(func.count()).select_from(delivery_type)
    res = session.execute(query).scalar()
    values_list = [{'id': 1, 'enum': 'dbs', 'name': 'Доставка на склад Wildberries'},
                   {'id': 2, 'enum': 'fbs', 'name': 'Доставка силами продавца'}, ]
    if res == 0:
        query = insert(delivery_type).values(values_list)
        session.execute(query)
        session.commit()


def save_order(item):
    query = select(order)
    res = session.execute(query).all()
    print(res)
    if not res:
        query = insert(order).values(item.dict())
        session.execute(query)
        session.commit()


def save_order_item(item):
    query = select(order_item).where(order_item.c.nmId == item.nmId)
    res = session.execute(query).scalar()
    if not res:
        query = insert(order_item).values(item.dict())
        session.execute(query)
        session.commit()


def save(item):
    insert_stmt = insert(order).values(item)
    do_update_stmt = insert_stmt.on_conflict_do_update(
        index_elements=['id'],
        set_=item)
    session.execute(do_update_stmt)


def get_wb_order():
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
                # save_order(item_head)
                # save_order_item(order_row)
                item_list.append(item_head.dict())
                save(item_head.dict())
            session.commit()

# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-on-conflict-insert