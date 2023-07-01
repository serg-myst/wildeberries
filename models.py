from sqlalchemy import Table, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
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
    Column('nmID', Integer, ForeignKey(good.c.id)),
    Column('price', Integer),
    Column('discount', Integer),
    Column('promoCode', Integer),
)
