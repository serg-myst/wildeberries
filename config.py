from dotenv import load_dotenv
import os

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