from dotenv import load_dotenv
import os
import logging

load_dotenv()

TOKEN = os.environ.get('TOKEN')

# end point
ORDERS_URL = 'https://suppliers-api.wildberries.ru/api/v3/orders/new'
OFFICES_URL = 'https://suppliers-api.wildberries.ru/api/v3/offices'
WAREHOUSES_URL = 'https://suppliers-api.wildberries.ru/api/v3/warehouses'
PRICES_URL = 'https://suppliers-api.wildberries.ru/public/api/v1/info'
GOODS_URL = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'

GOODS_QUERY = {
    "sort": {
        "cursor": {
            "limit": 1000
        },
        "filter": {
            "withPhoto": -1
        }
    }
}

# Логирование
FILE_LOG = 'wildberries_api.log'
logging.basicConfig(level=logging.INFO, filename=FILE_LOG,
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')
LOGGER = logging.getLogger('wildberries')

# Отправк, получение почты
MAIL_FROM = os.environ.get('MAIL_FROM')
MAIL_TO = os.environ.get('MAIL_TO')
PASSWORD = os.environ.get('PASSWORD')
SMTP = os.environ.get('SMTP')
SMTP_PORT = os.environ.get('SMTP_PORT')

