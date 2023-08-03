import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import MAIL_FROM, MAIL_TO, SMTP, SMTP_PORT, PASSWORD
from jinja2 import Environment, FileSystemLoader
from models import order, new_order, order_item, exchange, good, delivery_type, warehouse, office, currency
from database import session_maker
from sqlalchemy import select, update, alias
from config import LOGGER as log
from config import CURRENCY_CODES
from datetime import datetime

session = session_maker()


def mail_body():
    currency_1 = alias(currency)
    currency_2 = alias(currency)
    query = session.query(new_order.c.orderId, order.c.createdAt, order.c.orderUid, delivery_type.c.enum,
                          order_item.c.price, order_item.c.convertedPrice, (currency_1.c.code).label('currencyCode'),
                          (currency_2.c.code).label('convertedCurrencyCode'),
                          good.c.id, good.c.vendorCode,
                          good.c.object, warehouse.c.name, office.c.address).where(
        new_order.c.send == 0).order_by(order.c.createdAt)
    query = query.join(order, order.c.id == new_order.c.orderId)
    query = query.join(delivery_type, delivery_type.c.id == order.c.deliveryType)
    query = query.join(warehouse, warehouse.c.id == order.c.warehouseId)
    query = query.join(order_item, order_item.c.orderId == order.c.id)
    query = query.join(good, good.c.id == order_item.c.nmId)
    query = query.join(office, office.c.id == warehouse.c.office)
    query = query.join(currency_1, currency_1.c.code == order_item.c.currencyCode)
    query = query.join(currency_2, currency_2.c.code == order_item.c.convertedCurrencyCode)
    res = query.all()

    msg_body = ''
    order_id = ''
    orders_list = []
    orders_id = []
    for index, row in enumerate(res):
        if order_id == row.orderId:
            item = orders_list[index - 1]
            item['items'].append({'id': row.id, 'name': row.vendorCode, 'type': row.object, 'price': row.price / 100,
                                  'converted_price': row.convertedPrice / 100,
                                  'currency_code_html': CURRENCY_CODES.get(row.currencyCode),
                                  'currency_code': row.currencyCode,
                                  'converted_currency_code_html': CURRENCY_CODES.get(row.convertedCurrencyCode),
                                  'converted_currency_code': CURRENCY_CODES.get(row.convertedCurrencyCode)})
            item['total'] += row.price / 100
            item['converted_total'] += row.price / 100
        else:
            item_list = []
            item_list.append(
                {'id': row.id, 'name': row.vendorCode, 'type': row.object, 'price': row.price / 100,
                 'converted_price': row.convertedPrice / 100,
                 'currency_code_html': CURRENCY_CODES.get(row.currencyCode),
                 'currency_code': row.currencyCode,
                 'converted_currency_code_html': CURRENCY_CODES.get(row.convertedCurrencyCode),
                 'converted_currency_code': row.convertedCurrencyCode})
            item = {
                'number': row.orderId,
                'date': row.createdAt,
                'uid': row.orderUid,
                'type': row.enum,
                'address': row.address,
                'warehouse': row.name,
                'items': item_list,
                'total': row.price / 100,
                'converted_total': row.convertedPrice / 100,
                'currency_code': CURRENCY_CODES.get(row.currencyCode)
            }
            orders_list.append(item)
            orders_id.append(row.orderId)
        order_id = row.orderId

    if len(orders_list) > 0:
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template('mail.htm')

        delivery_query = select(delivery_type).order_by('enum')
        delivery_res = session.execute(delivery_query).all()

        msg_body = template.render(orders=orders_list, delivery=delivery_res)
    return msg_body, orders_id


def send_mail():
    query = select(exchange)
    res = session.execute(query).scalar()
    if res == 0:
        msg_body, orders = mail_body()
        if msg_body != '':
            try:
                msg = MIMEMultipart('alternative')  # Создаем сообщение
                msg['From'] = MAIL_FROM  # Отправитель
                msg['To'] = MAIL_TO  # Получатель
                msg['Subject'] = 'Заказы к сборке Wildberries'  # Тема сообщения

                msg.attach(MIMEText(msg_body, 'html'))  # Добавляем в сообщение HTML-фрагмент

                server = smtplib.SMTP(SMTP, SMTP_PORT)  # Создаем объект SMTP
                server.starttls()
                server.login(MAIL_FROM, PASSWORD)
                server.send_message(msg)
                server.quit()

                for item in orders:
                    query = update(new_order).values({'send': True, 'sendAt': datetime.now()}).where(
                        new_order.c.orderId == item)
                    session.execute(query)
                session.commit()
                log.info(f'Отправили новые заказы на почту {orders}')
            except SMTPException as e:
                log.exception(f'Ошибка отправки почты {e}')
        else:
            log.info(f'Отправка сообщения. Новые заказы не поступали!')


if __name__ == '__main__':
    pass
