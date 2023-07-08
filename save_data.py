from pydantic import ValidationError
from database import session_maker
from sqlalchemy import insert
from config import LOGGER as log
from models import order, order_item, new_order
from sqlalchemy.dialects.sqlite import insert
from schemas import Order, OrderItem, NewOrder

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


def get_wb_order(method):
    data_list = method()
    for data in data_list:
        try:
            item_head = Order(**data)
            order_row = OrderItem(**data)
            order_send = NewOrder(**data)
        except ValidationError as err:
            log.error(f'Данные не прошли по схеме. {err.json()}')
        else:
            save_data(item_head.dict(), order, ['id'])
            save_data(order_row.dict(), order_item, ['orderId', 'nmId'])
            save_data(order_send.dict(), new_order, ['orderId'])
    session.commit()

# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-on-conflict-insert
