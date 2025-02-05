from dotenv import load_dotenv
import os
import logging

load_dotenv()

TOKEN = os.environ.get('TOKEN')

# end point
ORDERS_URL = os.environ.get('ORDERS_URL')
ORDERS_ALL_URL = os.environ.get('ORDERS_ALL_URL')
OFFICES_URL = os.environ.get('OFFICES_URL')
WAREHOUSES_URL = os.environ.get('WAREHOUSES_URL')
PRICES_URL = os.environ.get('PRICES_URL')
GOODS_URL = os.environ.get('GOODS_URL')

GOODS_QUERY = {
    "settings": {
        "cursor": {
            "limit": 100
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

