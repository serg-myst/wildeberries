import datetime

from sqlalchemy import Table, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint, Date
from sqlalchemy import MetaData
from sqlalchemy.orm import registry, relationship

metadata = MetaData()
mapper_registry = registry()

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


class Office:
    def __repr__(self):
        return f'name={self.name}'


warehouse = Table(
    'warehouse',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('office', Integer, ForeignKey(office.c.id)),
    Column('name', String),
)


class Warehouse:
    def __repr__(self):
        return f'id={self.id} - {self.name}'


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


class Good:
    def __repr__(self):
        return f'id={self.id} - {self.object}'


price = Table(
    'price',
    metadata,
    Column('nmID', Integer, ForeignKey(good.c.id), primary_key=True),
    Column('price', Integer),
    Column('discount', Integer),
    Column('promoCode', Integer),
)


class Price(object):
    def __repr__(self):
        return f'id={self.nmID} - {self.price}'


delivery_type = Table(
    'delivery_type',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('enum', String),
    Column('name', String),
)


class DeliveryType:
    def __repr__(self):
        return f'{self.name}'


order = Table(
    'order_head',
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


class Order:
    def __repr__(self):
        return f'id={self.id} - {self.createdAt}'


currency = Table(
    'currency',
    metadata,
    Column('code', String, primary_key=True),
    Column('name', String, unique=True),
    Column('full_name', String, unique=True),
)


class Currency:
    def __repr__(self):
        return f'{self.name}'


order_item = Table(
    'order_item',
    metadata,
    Column('orderId', Integer, ForeignKey(order.c.id)),
    Column('nmId', Integer, ForeignKey(good.c.id)),
    Column('price', Integer),  # Цена в валюте продажи с учетом всех скидок, умноженная на 100
    Column('convertedPrice', Integer),  # Цена в валюте продажи с учетом всех скидок, умноженная на 100
    Column('currencyCode', ForeignKey(currency.c.code)),
    Column('convertedCurrencyCode', ForeignKey(currency.c.code)),
    Column('isLargeCargo', Boolean),
    PrimaryKeyConstraint('orderId', 'nmId', name='id'),
)


class OrderItem:
    def __repr__(self):
        return f'order id={self.orderId} good={self.nmId}'


new_order = Table(
    'new_order',
    metadata,
    Column('orderId', Integer, ForeignKey(order.c.id), primary_key=True),
    Column('send', Boolean, default=False),
    Column('sendAt', DateTime),
)

class NewOrder:
    def __repr__(self):
        return f'new order id={self.orderId}'


exchange = Table(
    'exchange',
    metadata,
    Column('is_started', Integer),  # 0 - обмен не запущен, 1 - обмен запущен
)

price_history = Table(
    'price_history',
    metadata,
    Column('period', Date, default=datetime.date),
    Column('nmId', Integer, ForeignKey(good.c.id)),
    Column('price', Integer),
    Column('discount', Integer),
    Column('promoCode', Integer),
    Column('id', Integer, primary_key=True)
)

class PriceHistory:
    def __repr__(self):
        return f'good={self.nmId} period={self.period} price={self.price}'


mapper_registry.map_imperatively(Price, price, properties={
    'good': relationship(Good, back_populates="prices")
})
mapper_registry.map_imperatively(Good, good, properties={
    'prices': relationship(Price, back_populates="good"),
    'price_history': relationship(PriceHistory, back_populates="good")
})
mapper_registry.map_imperatively(Order, order, properties={
    'items': relationship(OrderItem, back_populates="order"),
    'warehouse': relationship(Warehouse),
    'delivery_type': relationship(DeliveryType)
})
mapper_registry.map_imperatively(OrderItem, order_item, properties={
    'order': relationship(Order, back_populates="items"),
    'good': relationship(Good),
    'currency': relationship(Currency, foreign_keys='OrderItem.currencyCode'),
    'converted_currency': relationship(Currency, foreign_keys='OrderItem.convertedCurrencyCode')
})
mapper_registry.map_imperatively(NewOrder, new_order, properties={
    'order': relationship(Order)
})
mapper_registry.map_imperatively(Office, office)
mapper_registry.map_imperatively(Currency, currency)
mapper_registry.map_imperatively(Warehouse, warehouse, properties={
    'delivery_office': relationship(Office),
})
mapper_registry.map_imperatively(DeliveryType, delivery_type)
mapper_registry.map_imperatively(PriceHistory, price_history, properties={
    'good': relationship(Good, back_populates="price_history")
})
