from pydantic import BaseModel

class Book(BaseModel):
    name: str
    author_id: int
    genre_id: int
    language_id: int

class Author(BaseModel):
    name: str

class Genre(BaseModel):
    name: str

class Language(BaseModel):
    name: str

class BookLocation(BaseModel):
    location: str

class BookHistory(BaseModel):
    book_id: int
    user_id: int