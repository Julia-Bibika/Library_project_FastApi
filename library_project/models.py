from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Authors(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(124))
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return self.__dict__

class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(124))
    author_id = Column(Integer, ForeignKey("authors.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))
    language_id = Column(Integer, ForeignKey("languages.id"))
    authors = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    language = relationship("Language", back_populates="books")
    history = relationship("BookHistory", back_populates="book")
    locations = relationship("BookLocation", back_populates="book")


    def __repr__(self):
        return self.__dict__


class BookHistory(Base):
    tablename = "book_history"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    checked_out = Column(DateTime)
    checked_in = Column(DateTime)
    user = relationship("User", back_populates="books")
    book = relationship("Book", back_populates="history")

def __repr__(self):
        return self.__dict__

class Users(Base):
    __tablename__ = "users"
    username = Column(String(124))
    email = Column(String(124))
    full_name = Column(String(124))
    books = relationship("BookHistory", back_populates="user")


    def __repr__(self):
        return self.__dict__

class BookLocation(Base):
    tablename = "book_locations"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    location = Column(String)
    timestamp = Column(DateTime)
    book = relationship("Book", back_populates="locations")


    def __repr__(self):
        return self.__dict__


class Book(BaseModel):
    title: str
    author: int

class Author(BaseModel):
    id: int
    name: str

class Genre(BaseModel):
    name: str

class Language(BaseModel):
    name: str

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str
