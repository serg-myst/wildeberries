from schemas import Office, Good, Price
import json
from pprint import pprint
from pydantic import ValidationError
from database import session_maker
from models import office, good, price
from sqlalchemy import insert, update, select
import logging
from api import get_price_api, get_goods_api


def save_office(item):
    with session_maker() as session:
        query = select(office).where(office.c.id == item.id)
        obj = session.execute(query).all()
        if not obj:
            stmt = insert(office).values(**item.dict())
        else:
            stmt = update(office).where(office.c.id == item.id).values(**item.dict())
        session.execute(stmt)
        session.commit()


def save_good(item):
    with session_maker() as session:
        query = select(good).where(good.c.id == item.id)
        obj = session.execute(query).all()
        if not obj:
            stmt = insert(good).values(**item.dict())
        else:
            stmt = update(good).where(good.c.id == item.id).values(**item.dict())
        session.execute(stmt)
        session.commit()


def save_prices(item):
    with session_maker() as session:
        query = select(good).where(good.c.id == item.nmID)
        obj_good = session.execute(query).all()
        if obj_good:
            query = select(price).where(price.c.nmID == item.nmID)
            obj = session.execute(query).all()
            if not obj:
                stmt = insert(price).values(**item.dict())
            else:
                stmt = update(price).where(price.c.nmID == item.nmID).values(**item.dict())
            session.execute(stmt)
            session.commit()


def get_wb_offices():
    file_name = 'response_1687945801811.json'
    with open(file_name, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
        for data in data_list:
            try:
                item = Office(**data)
            except ValidationError as err:
                pprint(err.json())
            else:
                save_office(item)


def get_wb_goods():
    data_list = get_goods_api()
    for data in data_list:
        try:
            item = Good(**data)
        except ValidationError as err:
            pprint(err.json())
        else:
            save_good(item)


def get_wb_prices():
    data_list = get_price_api()
    for data in data_list:
        try:
            item = Price(**data)
        except ValidationError as err:
            pprint(err.json())
        else:
            save_prices(item)


if __name__ == '__main__':
    # get_wb_offices()
    get_wb_goods()
    # get_wb_prices()

# https://ru.stackoverflow.com/questions/631587/%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0-%D1%81-%D0%B1%D0%BE%D0%BB%D1%8C%D1%88%D0%B8%D0%BC-%D0%BA%D0%BE%D0%BB%D0%B8%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%BE%D0%BC-%D0%B7%D0%B0%D0%BF%D0%B8%D1%81%D0%B5%D0%B9-%D0%B2-%D1%81%D0%B5%D1%81%D1%81%D0%B8%D0%B8
# Запросы insert, update
