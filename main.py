from fastapi import FastAPI
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, create_engine, select
from typing import Annotated

from sqlalchemy import func
from math import ceil
from fastapi import Query
from contextlib import asynccontextmanager
from create_data import create_test_data
from loguru import logger
from fastapi import Depends, FastAPI, HTTPException
from models import *
from base_models import *


# region Config
sql_table_name = "assignment"
sql_url = f"mysql+pymysql://root:steve123@localhost:3306/{sql_table_name}"

engine = create_engine(sql_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# region App
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with Session(engine) as session:
            region_exists = session.exec(select(Regions).limit(1)).first()
            if not region_exists:
                print("Run create_test_data.")
                create_test_data(session=session)
            else:
                print("NOT Run create_test_data.")

    except Exception as e:
        logger.error(f"Failed to load startup data: {e}")
    yield


app = FastAPI(lifespan=lifespan)


# region API
@app.get("/products/", response_model=PaginatedProductResponse)
async def get_products(
    session: SessionDep,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(
        default=10, ge=1, le=100, description="Number of items per page"
    ),
):
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
            .join(RentalPeriods, ProductPricings.rental_period_id == RentalPeriods.id)
            .where(ProductPricings.product_id == product.id)
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


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, session: SessionDep):
    # Get the product
    product = session.exec(select(Products).where(Products.id == product_id)).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

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
