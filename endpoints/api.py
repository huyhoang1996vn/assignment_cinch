from fastapi import APIRouter
from .products import product_router

api_router = APIRouter()
api_router.include_router(product_router)