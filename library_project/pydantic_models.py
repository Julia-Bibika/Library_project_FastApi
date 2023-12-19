from pydantic import BaseModel
class Book(BaseModel):
    name: str
    author: int
    genre: int
    language: int

class Author(BaseModel):
    name: str

class Genre(BaseModel):
    name: str

class Language(BaseModel):
    name: str

class User(BaseModel):
    username : str
    email : str
    full_name : str
    disabled : bool

class UserInDB(User):
    hashed_password: str