import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import MAIL_FROM, MAIL_TO, SMTP, SMTP_PORT, PASSWORD
from jinja2 import Environment, FileSystemLoader
from models import order, new_order, order_item, exchange, good, delivery_type, warehouse, office
from database import session_maker
from sqlalchemy import select
from config import LOGGER as log

session = session_maker()


def mail_body():
    query = session.query(new_order.c.orderId, order.c.createdAt, order.c.orderUid, delivery_type.c.enum,
                          order_item.c.price, good.c.id, good.c.vendorCode,
                          good.c.object, warehouse.c.name, office.c.address).where(
        new_order.c.send == 0).order_by(order.c.createdAt).group_by(order.c.id, order_item.c.nmId)
    query = query.join(order, order.c.id == new_order.c.orderId)
    query = query.join(delivery_type, delivery_type.c.id == order.c.deliveryType)
    query = query.join(warehouse, warehouse.c.id == order.c.warehouseId)
    query = query.join(order_item, order_item.c.orderId == order.c.id)
    query = query.join(good, good.c.id == order_item.c.nmId)
    query = query.join(office, office.c.id == warehouse.c.office)
    res = query.all()

    msg_body = ''
    order_id = ''
    orders_list = []
    for row in res:
        if order_id == row.orderId:
            item = orders_list[len(orders_list) - 1]
            item['items'].append({'id': row.id, 'name': row.vendorCode, 'type': row.object, 'price': row.price / 100})
            item['total'] += row.price / 100
        else:
            item_list = []
            item_list.append(
                {'id': row.id, 'name': row.vendorCode, 'type': row.object, 'price': row.price / 100})
            item = {
                'number': row.orderId,
                'date': row.createdAt,
                'uid': row.orderUid,
                'type': row.enum,
                'address': row.address,
                'warehouse': row.name,
                'items': item_list,
                'total': row.price / 100
            }
            orders_list.append(item)
        order_id = row.orderId

    if len(orders_list) > 0:
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template('mail.htm')

        msg_body = template.render(orders=orders_list)

    return msg_body


def send_mail():
    query = select(exchange)
    res = session.execute(query).scalar()
    if res == 0:
        msg_body = mail_body()

        if msg_body != '':
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


if __name__ == '__main__':
    send_mail()
