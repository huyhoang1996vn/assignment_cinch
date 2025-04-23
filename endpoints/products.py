from math import ceil

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy import func
from sqlmodel import select

from endpoints.base_models import *
from models import *
from settings import SessionDep

product_router = APIRouter(tags=["Product"])


# region API
@product_router.get("/products/", response_model=PaginatedProductResponse)
async def get_products(
    session: SessionDep,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(
        default=10, ge=1, le=100, description="Number of items per page"
    ),
    region: str = Query(default=None, description="Region (eg: MY, SG)"),
    period: str = Query(default=None, description="Period (Month: 3,6,12)"),
):
    try:

        # Calculate offset
        offset = (page - 1) * page_size
        total_count = session.exec(select(func.count(Products.id))).one()
        total_pages = ceil(total_count / page_size)

        # Get paginated products
        products = session.exec(select(Products).offset(offset).limit(page_size)).all()

        response_data = []

        for product in products:
            # Get attributes for this product
            attributes = session.exec(
                select(Attributes).where(Attributes.product_id == product.id)
            ).all()

            # Get pricing information with region and rental period details
            pricing_query = (
                select(ProductPricings, Regions, RentalPeriods)
                .join(Regions, ProductPricings.region_id == Regions.id)
                .join(
                    RentalPeriods, ProductPricings.rental_period_id == RentalPeriods.id
                )
                .where(ProductPricings.product_id == product.id)
            )
            if region:
                pricing_query = pricing_query.where(Regions.code == region)
            if period:
                pricing_query = pricing_query.where(RentalPeriods.month == period)

            pricing_results = session.exec(pricing_query).all()

            # Format pricing data
            pricing_data = [
                PricingResponse(
                    rental_period_months=rental_period.month,
                    price=pricing.price,
                    region_name=region.name,
                    region_code=region.code,
                )
                for pricing, region, rental_period in pricing_results
            ]

            # Format attributes
            attribute_data = [
                AttributeResponse(name=attr.name, value=attr.value)
                for attr in attributes
            ]

            # Create the product response
            product_response = ProductResponse(
                id=product.id,
                name=product.name,
                description=product.description,
                sku=product.sku,
                detail=product.detail,
                attributes=attribute_data,
                pricing=pricing_data,
            )

            response_data.append(product_response)

        return PaginatedProductResponse(
            current_page=page,
            page_size=page_size,
            total_items=total_count,
            total_pages=total_pages,
            items=response_data,
        )
    except Exception as e:
        logger.error(f"Exception in get_products: {e}")
        return JSONResponse(
            content={"detail": {e}}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@product_router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, session: SessionDep):
    try:
        # Get the product
        product = session.exec(
            select(Products).where(Products.id == product_id)
        ).first()

        if not product:
            return JSONResponse(status_code=404, content="Product not found")

        # Get attributes
        attributes = session.exec(
            select(Attributes).where(Attributes.product_id == product_id)
        ).all()

        # Get pricing information
        pricing_query = (
            select(ProductPricings, Regions, RentalPeriods)
            .join(Regions, ProductPricings.region_id == Regions.id)
            .join(RentalPeriods, ProductPricings.rental_period_id == RentalPeriods.id)
            .where(ProductPricings.product_id == product_id)
        )

        pricing_results = session.exec(pricing_query).all()

        # Format pricing data
        pricing_data = [
            PricingResponse(
                rental_period_months=rental_period.month,
                price=pricing.price,
                region_name=region.name,
                region_code=region.code,
            )
            for pricing, region, rental_period in pricing_results
        ]

        # Format attributes
        attribute_data = [
            AttributeResponse(name=attr.name, value=attr.value) for attr in attributes
        ]

        # Create and return the response
        return ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            sku=product.sku,
            detail=product.detail,
            attributes=attribute_data,
            pricing=pricing_data,
        )
    except Exception as e:
        logger.error(f"Exception in get_product: {e}")
        return JSONResponse(
            content={"detail": {e}}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@product_router.get("/regions", response_model=List[ResgionResponse])
async def get_regions(session: SessionDep):
    try:
        regions = session.exec(select(Regions)).all()
        return regions
    except Exception as e:
        logger.error(f"Exception in get_regions: {e}")
        return JSONResponse(
            content={"detail": {e}}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
