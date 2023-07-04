from save_data import get_wb_data
from models import office, warehouse, good, price
from schemas import Office, Warehouse, Good, Price
from api import get_office_api, get_warehouse_api, get_goods_api, get_price_api
from config import LOGGER as log
from save_data import fill_delivery, get_wb_order

if __name__ == '__main__':
    log.info(f'API. Начало получения данных.')
    fill_delivery()
    get_wb_data(office, Office, get_office_api)
    get_wb_data(warehouse, Warehouse, get_warehouse_api)
    get_wb_data(good, Good, get_goods_api)
    get_wb_data(price, Price, get_price_api, 'nmId')
    # get_wb_order()
    log.info(f'API. Окончание получения данных.')

# https://ru.stackoverflow.com/questions/631587/%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0-%D1%81-%D0%B1%D0%BE%D0%BB%D1%8C%D1%88%D0%B8%D0%BC-%D0%BA%D0%BE%D0%BB%D0%B8%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%BE%D0%BC-%D0%B7%D0%B0%D0%BF%D0%B8%D1%81%D0%B5%D0%B9-%D0%B2-%D1%81%D0%B5%D1%81%D1%81%D0%B8%D0%B8
# Запросы insert, update
