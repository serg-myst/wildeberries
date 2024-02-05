from database import session_maker
from sqlalchemy import select, update
from models import logs_table
import telebot
from config import BOT_ID, USER_ID
from datetime import datetime

session = session_maker()
bot = telebot.TeleBot(BOT_ID)


def get_errors():
    query = select(logs_table).where(logs_table.c.send == False)
    res = session.execute(query).all()
    return res


def send_message():
    res = get_errors()
    user_id = USER_ID.split(',')
    if len(res) != 0:
        for mes in res:
            for uid in user_id:
                if uid != '':
                    bot.send_message(uid, f'Время лог. = {mes[1]}. Текст = {mes[2]}')
            query = update(logs_table).values({'send': True, 'send_at': datetime.now()}).where(
            logs_table.c.id == mes.id)
            session.execute(query)
            session.commit()


if __name__ == '__main__':
    pass
