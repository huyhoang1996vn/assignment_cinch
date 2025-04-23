from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from sqlmodel import Session, select

from create_data import create_test_data
from endpoints.api import api_router
from models import Regions
from settings import engine


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
app.include_router(api_router)

