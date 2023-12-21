from datetime import timedelta, datetime
from typing import Annotated, List, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from session import get_session
from crud.auth import *

from pydantic_models import Token, UserFull, UserCreating, TokenData

auth_router = APIRouter()

SECRET_KEY = "034d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db_session, username: str, password: str):
    user = get_user_by_username(db_session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        db_session: Annotated[Session, Depends(get_session)],
        token: Annotated[str, Depends(oauth2_scheme)]
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
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db_session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def is_admin(
    current_active_user: Annotated[User, Depends(get_current_active_user)]
):
    if not current_active_user.is_admin:
        raise HTTPException(status_code=400, detail="Not enough rights")
    return current_active_user


@auth_router.get("/")
def root():
    return {"message": "Hello auth"}


@auth_router.get("/users", response_model=List[UserFull])
def get_users(
        db_session: Annotated[Session, Depends(get_session)]
        ):
    return get_users_from_db(db_session)


@auth_router.post("/users", response_model=Union[UserFull, None])
def add_user(
        user: UserCreating,
        db_session: Annotated[Session, Depends(get_session)]
):
    user.password = get_password_hash(user.password)
    return add_user_to_db(db_session, user)


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    db_session:  Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(db_session, form_data.username, form_data.password)
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
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users/me/",  response_model=UserFull)
async def read_users_me(
    current_user: Annotated[User, Depends(is_admin)]
):
    return current_user