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
from models import *
# from sqlalchemy.ext.declarative import declarative_base

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Base = declarative_base()

# region BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


class UserInDB(User):
    hashed_password: str




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

# region SQLite
# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
sqlite_file_name = "assignment"
sqlite_url = f"mysql+pymysql://root:steve123@localhost:3306/{sqlite_file_name}"

# connect_args = {"echo": True}
engine = create_engine(sqlite_url, echo=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

# region App
app = FastAPI()


class UserModel(BaseModel):
    username: str
    password: str
    email: EmailStr


@app.on_event("startup")
def on_startup():
    # create_db_and_tables()
    pass

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


@app.post("/comments")
def post_comments(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/comments")
def get_comments(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
