from dotenv import load_dotenv
import os
import logging

load_dotenv()

TOKEN = os.environ.get('TOKEN')

# end point
ORDERS_URL = 'https://suppliers-api.wildberries.ru/api/v3/orders/new'
ORDERS_ALL_URL = 'https://suppliers-api.wildberries.ru/api/v3/orders'
OFFICES_URL = 'https://suppliers-api.wildberries.ru/api/v3/offices'
WAREHOUSES_URL = 'https://suppliers-api.wildberries.ru/api/v3/warehouses'
PRICES_URL = 'https://suppliers-api.wildberries.ru/public/api/v1/info'
GOODS_URL = 'https://content-api.wildberries.ru/content/v2/get/cards/list?locale=ru'

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

# Отправка, получение почты
MAIL_FROM = os.environ.get('MAIL_FROM')
MAIL_TO = os.environ.get('MAIL_TO')
PASSWORD = os.environ.get('PASSWORD')
SMTP = os.environ.get('SMTP')
SMTP_PORT = os.environ.get('SMTP_PORT')

# Database connection
DATABASE = os.environ.get('DATABASE_URL')

# Base type
BASE_TYPE = os.environ.get('USE_BASE')

# Bot
BOT_ID = os.environ.get('BOT')
USER_ID = os.environ.get('USER_ID')

# HTML code currency
CURRENCY_CODES = {
    '643': '&#8381;',
    '051': '&#1423;',
    '933': 'Br',
    '398': '&#8376;',
    '417': 'сом',
    '860': 'сўм',
}

# Currencies for fill_db
CURRENCIES = [
        {
            'code': '643',
            'name': 'RUB',
            'full_name': 'Российский рубль'
        },
        {
            'code': '051',
            'name': 'AMD',
            'full_name': 'Армянский драм'
        },
        {
            'code': '933',
            'name': 'BYN',
            'full_name': 'Белорусский рубль'
        },
        {
            'code': '398',
            'name': 'KZT',
            'full_name': 'Тенге'
        },
        {
            'code': '417',
            'name': 'KGS',
            'full_name': 'Сом'
        },
        {
            'code': '860',
            'name': 'UZS',
            'full_name': 'Узбекский сум'
        },
    ]

