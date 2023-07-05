from sqlalchemy import insert, select, func
from database import session_maker
from models import delivery_type, exchange

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


if __name__ == '__main__':
    fill_delivery()
    fill_exchange()
