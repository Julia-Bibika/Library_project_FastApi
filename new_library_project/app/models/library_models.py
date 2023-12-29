from sqlalchemy import Column, Integer, String, ForeignKey,DateTime, func
from app.session import Base

class Authors(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(124))

class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(124))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))
    language_id = Column(Integer, ForeignKey("languages.id"))
    book_location = Column(String(50), default='None location')


class BookHistories(Base):
    __tablename__ = "book-histories"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    checked_out = Column(DateTime, server_default=func.now())
    checked_in = Column(DateTime, server_default=func.now())

class BookLocations(Base):
    __tablename__ = "book-locations"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    location = Column(String(50), default='None location')
    timestamp = Column(DateTime, server_default=func.now())


class Genres(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(124))

class Languages(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(124))
