from pydantic import ValidationError
from database import session_maker
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from config import LOGGER as log
from models import order, order_item, new_order, logs_table
from sqlalchemy.dialects.sqlite import insert
from schemas import Order, OrderItem, NewOrder

session = session_maker()


def save_error(txt, is_error=True):
    stmt = insert(logs_table).values(logtext=txt, is_error=is_error, send=False)
    session.execute(stmt)
    session.commit()


def save_data(item, table, id):
    try:
        insert_stmt = insert(table).values(item)
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=id,
            set_=item)
        session.execute(do_update_stmt)
    except SQLAlchemyError as err:
        save_error(str(err))


def get_wb_data(table, model, method, id=None):
    if id is None:
        id = ['id']
    data_list = method()
    for data in data_list:
        try:
            item = model(**data)
        except ValidationError as err:
            err_txt = f'Данные не прошли по схеме. {err.json()}'
            save_error(err_txt)
            log.error(err_txt)
        else:
            save_data(item.dict(), table, id)
    try:
        session.commit()
    except SystemError as e:
        err_txt = f'Ошибка записи данных по {table}. {e}'
        save_error(err_txt)
        log.error(err_txt)


def get_wb_order(method, send=True):
    data_list = method()
    for data in data_list:
        try:
            item_head = Order(**data)
            order_row = OrderItem(**data)
            order_send = NewOrder(**data)
        except ValidationError as err:
            err_txt = f'Данные не прошли по схеме. {err.json()}'
            save_error(err_txt)
            log.error(err_txt)
        else:
            save_data(item_head.dict(), order, ['id'])
            save_data(order_row.dict(), order_item, ['orderId', 'nmId'])
            if send:
                save_data(order_send.dict(), new_order, ['orderId'])
    session.commit()


# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-on-conflict-insert

if __name__ == '__main__':
    pass
