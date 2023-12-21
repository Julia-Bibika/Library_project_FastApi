from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from session import engine

Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(124))
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return self.__dict__

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(124))
    author_id = Column(Integer, ForeignKey("authors.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))
    language_id = Column(Integer, ForeignKey("languages.id"))
    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    language = relationship("Language", back_populates="books")
    history = relationship("BookHistory", back_populates="book")
    locations = relationship("BookLocation", back_populates="book")

    def __repr__(self):
        return self.__dict__

class BookHistory(Base):
    __tablename__ = "book_history"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    checked_out = Column(DateTime)
    checked_in = Column(DateTime)
    user = relationship("User", back_populates="book_histories")
    book = relationship("Book", back_populates="history")

    def __repr__(self):
        return self.__dict__

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(124))
    email = Column(String(124), nullable=True)
    full_name = Column(String(124), nullable=True)
    is_admin = Column(Boolean, default=False)
    book_histories = relationship("UserHistory", back_populates="user")

    def __repr__(self):
        return self.__dict__

class UserHistory(Base):
    __tablename__ = "user_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="book_histories")

    def __repr__(self):
        return self.__dict__
class BookLocation(Base):
    __tablename__ = "book_locations"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    location = Column(String)
    timestamp = Column(DateTime)
    book = relationship("Book", back_populates="locations")

    def __repr__(self):
        return self.__dict__

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(124))
    books = relationship("Book", back_populates="genre")

    def __repr__(self):
        return self.__dict__

class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(124))
    books = relationship("Book", back_populates="language")

    def __repr__(self):
        return self.__dict__

Base.metadata.create_all(bind=engine)
