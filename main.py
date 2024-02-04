from save_data import get_wb_data, get_wb_order
from models import office, warehouse, good, price
from schemas import Office, Warehouse, Good, Price
from api import get_office_api, get_warehouse_api, get_goods_api, get_price_api, get_orders_api, get_orders_by_date_api
from config import LOGGER as log
from send_mail import send_mail
from sys import argv
from bot import send_message

if __name__ == '__main__':
    script, type_query = argv
    if type_query == 'n':
        log.info(f'API. Начало. Получаем НСИ. {script}')
        get_wb_data(office, Office, get_office_api)
        get_wb_data(warehouse, Warehouse, get_warehouse_api)
        get_wb_data(good, Good, get_goods_api)
        get_wb_data(price, Price, get_price_api, ['nmID'])
        log.info(f'API. Окончание. Получаем НСИ.')
    if type_query == 'o':
        log.info(f'API. Начало. Получаем новые заказы. {script}')
        get_wb_order(get_orders_api)
        log.info(f'API. Окончание. Получаем новые заказы.')
    if type_query == 's':
        log.info(f'API. Начало. Отправляем новые заказы. {script}')
        send_mail()
        log.info(f'API. Окончание. Отправляем новые заказы.')
    if type_query == 'os':
        log.info(f'API. Начало. Получаем/Отправляем новые заказы. {script}')
        get_wb_order(get_orders_api)
        get_wb_order(get_orders_by_date_api, False)
        send_mail()
        log.info(f'API. Окончание. Получаем/Отправляем новые заказы.')
    if type_query == 'm':
        send_message()

# https://ru.stackoverflow.com/questions/631587/%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0-%D1%81-%D0%B1%D0%BE%D0%BB%D1%8C%D1%88%D0%B8%D0%BC-%D0%BA%D0%BE%D0%BB%D0%B8%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%BE%D0%BC-%D0%B7%D0%B0%D0%BF%D0%B8%D1%81%D0%B5%D0%B9-%D0%B2-%D1%81%D0%B5%D1%81%D1%81%D0%B8%D0%B8
# Запросы insert, update
