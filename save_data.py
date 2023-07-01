from pprint import pprint
from pydantic import ValidationError
from database import session_maker
from sqlalchemy import insert, delete, select, update

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
        return True
    except:
        # Здесь должны быть логи
        return False


def get_wb_data(table, model, method):
    data_list = method()
    item_list = []
    for data in data_list:
        try:
            item = model(**data)
        except ValidationError as err:
            pprint(err.json())
        else:
            item_list.append(item.dict())
    if len(item_list) > 0:
        save_data(item_list, table)
