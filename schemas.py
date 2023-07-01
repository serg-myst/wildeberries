from pydantic import BaseModel, Field
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
