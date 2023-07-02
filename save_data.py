from pydantic import ValidationError
from database import session_maker
from sqlalchemy import insert, delete, select, update, func
from config import LOGGER as log
from models import delivery_type

session = session_maker()


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
