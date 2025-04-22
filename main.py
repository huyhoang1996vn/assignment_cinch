from fastapi import FastAPI
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
import jwt

from sqlalchemy import func
from math import ceil
from fastapi import Query
from contextlib import asynccontextmanager
from create_data import create_test_data
from loguru import logger
from fastapi import Depends, FastAPI, HTTPException, status
from models import *
from base_models import *

from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

# to get a string like this run:
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# region Authen
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(User):
    hashed_password: str


class UserModel(BaseModel):
    username: str
    password: str
    email: EmailStr


def get_user(session, username: str):
    user = session.exec(select(User).where(User.username == username)).one_or_none()
    return user


def authenticate_user(session, username: str, password: str):
    user = get_user(session, username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


# region API
@app.post("/register/")
def register(userModel: UserModel, session: SessionDep) -> User:
    user = User(username=userModel.username, email=userModel.email)
    user.set_password(userModel.password)  # Set the password
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"username": user.username, "email": user.email}


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
