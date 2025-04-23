from contextlib import asynccontextmanager
from math import ceil
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy import func
from sqlmodel import Session, create_engine, select

from create_data import create_test_data
from models import *
from settings import engine
from endpoints.api import api_router

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

