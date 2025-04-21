from typing import Union
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI
from typing import Annotated
import bcrypt
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy import UniqueConstraint, Column, String

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

metadata = SQLModel.metadata
# region SQLModel
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", String(100), unique=True))
    email: EmailStr
    hashed_password: str

    def set_password(self, password: str):
        """Hash the password and store it."""
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        """Verify the provided password against the stored hashed password."""
        return bcrypt.checkpw(
            password.encode("utf-8"), self.hashed_password.encode("utf-8")
        )