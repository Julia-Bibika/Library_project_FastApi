from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from sqlalchemy.orm import declarative_base

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
    authors = relationship("Author", back_populates="books")
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
    user = relationship("User", back_populates="books")
    book = relationship("Book", back_populates="history")

    def __repr__(self):
            return self.__dict__

# class User(Base):
#     __tablename__ = "users"
#     username = Column(String(124))
#     email = Column(String(124))
#     full_name = Column(String(124))
#     books = relationship("BookHistory", back_populates="user")
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(124))
    email = Column(String(124), nullable=True)
    full_name = Column(String(124), nullable=True)
    disabled = Column(Boolean, default=False)
    books = relationship("BookHistory", back_populates="user")

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


class UserInDB(User):
    hashed_password: str
