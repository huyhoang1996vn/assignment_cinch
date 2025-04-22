# Add these imports at the top of main.py
from typing import List, Optional
from pydantic import BaseModel


# Add these Pydantic models for the API response
class AttributeResponse(BaseModel):
    name: str
    value: str


class PricingResponse(BaseModel):
    rental_period_months: int
    price: int
    region_name: str
    region_code: str


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    sku: Optional[str]
    detail: Optional[str]
    attributes: List[AttributeResponse]
    pricing: List[PricingResponse]


class PaginationMeta(BaseModel):
    current_page: int
    page_size: int
    total_items: int
    total_pages: int


class PaginatedProductResponse(BaseModel):
    items: List[ProductResponse]
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
