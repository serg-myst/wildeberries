from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


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
    updateAt: datetime = Field(alias='updatedAt')
    vendorCode: str
    brand: str
    object: str = Field(alias='subjectName')
    imtID: int
    isProhibited: Optional[bool] = False


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
    supplyId: str | None = None
    address: str | None = None
    user: str | None = None
    orderUid: str
    deliveryType: str

    @validator('deliveryType')
    def set_deliveryType(cls, d: str) -> int:
        if d == 'dbs':
            return 1
        if d == 'fbs':
            return 2


class OrderItem(BaseModel):
    orderId: int = Field(alias='id')
    nmId: int
    price: int
    convertedPrice: int
    currencyCode: str
    convertedCurrencyCode: str
    isLargeCargo: Optional[bool] = False  # 23.10.2023 is optional

    @validator('currencyCode')
    def set_currencyCode(cls, cd: str) -> str:
        return cd.zfill(3)

    @validator('convertedCurrencyCode')
    def set_convertedCurrencyCode(cls, cd: str) -> str:
        return cd.zfill(3)


class NewOrder(BaseModel):
    orderId: int = Field(alias='id')
