from sqlalchemy import Table, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy import MetaData

metadata = MetaData()

office = Table(
    'office',
    metadata,
    Column('address', String),
    Column('name', String),
    Column('city', String),
    Column('id', Integer, primary_key=True),
    Column('longitude', Float),
    Column('latitude', Float),
    Column('selected', Boolean),
)

warehouse = Table(
    'warehouse',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('office', Integer, ForeignKey(office.c.id)),
    Column('name', String),
)

good = Table(
    'good',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('vendorCode', String),
    Column('brand', String),
    Column('object', String),
    Column('imtID', Integer),
    Column('isProhibited', Boolean),
    Column('updateAt', DateTime),
)

price = Table(
    'price',
    metadata,
    Column('nmID', Integer, ForeignKey(good.c.id), primary_key=True),
    Column('price', Integer),
    Column('discount', Integer),
    Column('promoCode', Integer),
)

delivery_type = Table(
    'delivery_type',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('enum', String),
    Column('name', String),
)

order = Table(
    'order',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('createdAt', DateTime),
    Column('warehouseId', ForeignKey(warehouse.c.id)),
    Column('rid', String),  # Идентификатор сборочного задания в системе Wildberries
    Column('supplyId', String),  # Идентификатор поставки. Возвращается, если заказ закреплён за поставкой
    Column('address', String),  # Aдрес покупателя для доставки
    Column('user', String),  # Aдрес покупателя для доставки
    Column('orderUid', String),  # Идентификатор транзакции для группировки сборочных заданий
    Column('deliveryType', ForeignKey(delivery_type.c.id)),
    # Тип доставки: fbs - доставка на склад Wildberries, dbs - доставка силами продавца
)

order_item = Table(
    'order_item',
    metadata,
    Column('orderId', Integer, ForeignKey(order.c.id)),
    Column('nmId', Integer, ForeignKey(good.c.id)),
    Column('price', Integer),  # Цена в валюте продажи с учетом всех скидок, умноженная на 100
    Column('isLargeCargo', Boolean),
    PrimaryKeyConstraint('orderId', 'nmId', name='id'),
)

new_order = Table(
    'new_order',
    metadata,
    Column('orderId', Integer, ForeignKey(order.c.id), primary_key=True),
    Column('send', Boolean),
    Column('sendAt', DateTime),
)

exchange = Table(
    'exchange',
    metadata,
    Column('is_started', Integer),  # 0 - обмен не запущен, 1 - обмен запущен
)
