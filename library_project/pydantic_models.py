from typing import Union

from pydantic import BaseModel
class BookValidation(BaseModel):
    name: str
    author_id: int
    genre_id: int
    language_id: int

class BookLocation(BaseModel):
    id : int
    book_id : int
    location : str
    timestamp : str

class AuthorValidation(BaseModel):
    name: str

class GenreValidation(BaseModel):
    name: str

class LanguageValidation(BaseModel):
    name: str

class User(BaseModel):
    username : str
    email : str
    full_name : str
    is_admin : bool

class UserInDB(User):
    hashed_password: str

class UserCreating(User):
    password: str

class UserFull(User):
    id: Union[int, None] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None