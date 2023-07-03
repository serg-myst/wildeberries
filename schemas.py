from pydantic import BaseModel, Field, validator
from datetime import datetime


class Office(BaseModel):
    address: str
    name: str
    city: str
    id: int
    longitude: float
    latitude: float
    selected: bool


class Warehouse(BaseModel):
    id: int
    office: int = Field(alias='officeId')
    name: str


class Good(BaseModel):
    id: int = Field(alias='nmID')
    updateAt: datetime
    vendorCode: str
    brand: str
    object: str
    imtID: int
    isProhibited: bool


class Price(BaseModel):
    nmID: int = Field(alias='nmId')
    price: int
    discount: int
    promoCode: int


class Order(BaseModel):
    id: int
    createdAt: datetime
    warehouseId: int
    rid: str
    supplyId: str
    address: str
    user: str
    orderUid: str
    deliveryType: int

    @validator('deliveryType')
    def set_deliveryType(cls, d: str) -> str:
        if d == 'dbs':
            return 1
        if d == 'fbs':
            return 2
