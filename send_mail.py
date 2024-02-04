import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import MAIL_FROM, MAIL_TO, SMTP, SMTP_PORT, PASSWORD
from jinja2 import Environment, FileSystemLoader
from models import NewOrder, DeliveryType, exchange, new_order, Order, OrderItem
from database import session_maker
from sqlalchemy import select, update
from config import LOGGER as log
from config import CURRENCY_CODES
from datetime import datetime
from sqlalchemy.orm import selectinload
from save_data import save_error

session = session_maker()


def mail_body():
    query = (
        select(NewOrder).options(selectinload(NewOrder.order).
                                 joinedload(Order.items, innerjoin=True).
                                 joinedload(OrderItem.good, innerjoin=True)).
        where(NewOrder.send == False)
    )

    res = session.execute(query)
    result = res.scalars().all()

    msg_body = ''
    if len(result) > 0:
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template('mail.htm')
        delivery_query = select(DeliveryType).order_by('enum')
        delivery_res = session.execute(delivery_query).scalars().all()

        msg_body = template.render(orders=result, delivery=delivery_res, codes=CURRENCY_CODES)

    return msg_body, result


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
                        new_order.c.orderId == item.orderId)
                    session.execute(query)
                session.commit()
                mes_txt = f'Отправили новые заказы на почту {orders}'
                save_error(mes_txt, False)
                log.info(mes_txt)
            except SMTPException as e:
                err = f'Ошибка отправки почты {e}'
                save_error(err)
                log.exception(err)
        else:
            log.info(f'Отправка сообщения. Новые заказы не поступали!')


if __name__ == '__main__':
    pass
