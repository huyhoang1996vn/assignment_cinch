from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

metadata = SQLModel.metadata


class Products(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: Optional[str] = None
    sku: Optional[str] = None
    detail: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Attributes(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    value: str
    product_id: int | None = Field(foreign_key="products.id")


class Regions(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    code: str


class RentalPeriods(SQLModel, table=True):
    id: int = Field(primary_key=True)
    month: int


class ProductPricings(SQLModel, table=True):
    id: int = Field(primary_key=True)
    region_id: int = Field(foreign_key="regions.id")
    rental_period_id: int = Field(foreign_key="rentalperiods.id")
    product_id: int = Field(foreign_key="products.id")
    price: int
