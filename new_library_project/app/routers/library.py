from datetime import datetime

# import psycopg2
from typing import Annotated

# import dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.models.library_models import Books, Genres, Authors, Languages, BookLocations, BookHistories
from app.models.users import Users, UserHistories
from app.pydantic_models.library_model import Book, Genre, Author, Language, BookLocation, BookHistory
from app.pydantic_models.user import UserHistory
from app.routers.auth import get_current_user
from app.session import get_session

# dotenv.load_dotenv("../.env")
# conn_dict = {
#     "host": "localhost",
#     "user": "postgres",
#     "password": "21345",
#     "port": 5432,
#     "database":"library",
# }
#
# connection = psycopg2.connect(
#     **conn_dict
# )

library_router = APIRouter(prefix='/library', tags=['books'])
db_dependency = Annotated[Session, Depends(get_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Ендпоінт для отримання всіх книг
@library_router.get('/get_all_books')
def get_books(db_session: db_dependency):
    """
           Отримує список всіх книг у бібліотеці.

           Returns:
               books: Список об'єктів книг.
           """
    books = db_session.query(Books).all()
    return books

@library_router.get('/get_by_id')
def get_book_by_id(db_session: db_dependency, id):
    book = db_session.query(Books).filter(Books.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such book in db')
    return book

# Ендпоінт для додавання нової книги
@library_router.post('/create_book')
async def create_book(db_session: db_dependency, item: Book, user: user_dependency):
    """
           Додає нову книгу до бібліотеки.

           Args:
               item (Book): Об'єкт валідації книги.

           Returns:
               new_book : Створена нова книга
           """
    user_id = user[1]
    new_book = Books(name=item.name,user_id=user_id, author_id=item.author_id,genre_id=item.genre_id,language_id=item.language_id)
    db_session.add(new_book)
    db_session.commit()
    return new_book

# Ендпоінт для оновлення книги
@library_router.put('/update_book')
async def update_book(book_id, item: Book, db_session: db_dependency, user: user_dependency):
    """
              Оновлює книгу в бібліотеці.

              Args:
                  item (Book): Об'єкт валідації книги.
                  book_id (int): індетифікатор книги

              Returns:
                  book : Оновлена книга
              """
    user_id = user[1]
    user = db_session.query(Users).filter(Users.id == user_id).first()
    book = db_session.query(Books).filter(Books.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such book')
    if book.user_id == user_id or user.is_admin > 0:
        book.name = item.name
        book.author_id = item.author_id
        book.genre_id = item.genre_id
        book.language_id = item.language_id
        db_session.commit()
        return book
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail='You are a teapot')

# Ендпоінт для видалення книги
@library_router.delete('/delete_book')
async def delete_book(book_id, db_session: db_dependency, user: user_dependency):
    """
               Видаляє книгу в бібліотеці.

               Args:
                   book_id (int): індетифікатор книги

               Returns:
                   book : Видалена книга
               """
    user_id = user[1]
    user = db_session.query(Users).filter(Users.id == user_id).first()
    book = db_session.query(Books).filter(Books.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such book')
    if book.user_id == user_id or user.is_admin > 0:
        db_session.query(Books).filter(Books.id == book_id).delete()
        db_session.commit()
        return book
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail='You are a teapot')

# Ендпоінт для додавання нового жанру
@library_router.post('/create_genre')
async def create_genre(db_session: db_dependency, item: Genre, user: user_dependency):
    """
           Додає новий жанр до бібліотеки.

           Args:
               item (Genre): Об'єкт валідації жанру.

           Returns:
               new_genre : Створений новий жанр
           """
    user_id = user[1]
    new_genre = Genres(user_id=user_id,name=item.name)
    db_session.add(new_genre)
    db_session.commit()
    return new_genre

# Ендпоінт для оновлення жанру
@library_router.put('/update_genre')
async def update_genre(genre_id, item: Genre, db_session: db_dependency, user: user_dependency):
    """
              Оновлює жанр в бібліотеці.

              Args:
                  item (Genre): Об'єкт валідації жанру.
                  genre_id (int): індетифікатор жанру

              Returns:
                  genre : Оновлений жанр
              """
    user_id = user[1]
    user = db_session.query(Users).filter(Users.id == user_id).first()
    genre = db_session.query(Genres).filter(Genres.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such genre')
    if genre.user_id == user_id or user.is_admin > 0:
        genre.name = item.name
        db_session.commit()
        return genre
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail='You are a teapot')

# Ендпоінт для видалення жанру
@library_router.delete('/delete_genre')
async def delete_genre(genre_id, db_session: db_dependency, user: user_dependency):
    """
               Видаляє жанр з бібліотеки.

               Args:
                   genre_id (int): індетифікатор жанру

               Returns:
                  genre : Видалений жанр
               """
    user_id = user[1]
    user = db_session.query(Users).filter(Users.id == user_id).first()
    genre = db_session.query(Genres).filter(Genres.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such genre')
    if genre.user_id == user_id or user.is_admin > 0:
        db_session.query(Genres).filter(Genres.id == genre_id).delete()
        db_session.commit()
        return genre
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail='You are a teapot')

# Ендпоінт для додавання нового автору
@library_router.post('/create_author')
async def create_author(db_session: db_dependency, item: Author, user: user_dependency):
    """
           Додає нового автора до бібліотеки.

           Args:
               item (Author): Об'єкт валідації автора.

           Returns:
               new_author : Створений новий автор
           """
    user_id = user[1]
    new_author = Authors(user_id=user_id,name=item.name)
    db_session.add(new_author)
    db_session.commit()
    return new_author

# Ендпоінт для оновлення автора
@library_router.put('/update_author')
async def update_author(author_id, item: Author, db_session: db_dependency, user: user_dependency):
    """
              Оновлює автора в бібліотеці.

              Args:
                  item (Author): Об'єкт валідації автора.
                  author_id (int): індетифікатор автора

              Returns:
                  author : Оновлений автор
              """
    user_id = user[1]
    user = db_session.query(Users).filter(Users.id == user_id).first()
    author = db_session.query(Authors).filter(Authors.id == author_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such author')
    if author.user_id == user_id or user.is_admin > 0:
        author.name = item.name
        db_session.commit()
        return author
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail='You are a teapot')

# Ендпоінт для видалення автора
@library_router.delete('/delete_author')
async def delete_author(author_id, db_session: db_dependency, user: user_dependency):
    """
               Видаляє автора в бібліотеці.

               Args:
                   author_id (int): індетифікатор автора

               Returns:
                  author : Видалений автор
               """
    user_id = user[1]
    user = db_session.query(Users).filter(Users.id == user_id).first()
    author = db_session.query(Authors).filter(Authors.id == author_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such author')
    if author.user_id == user_id or user.is_admin > 0:
        db_session.query(Authors).filter(Authors.id == author_id).delete()
        db_session.commit()
        return author
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail='You are a teapot')

# Ендпоінт для додавання нової мови
@library_router.post('/create_language')
async def create_language(db_session: db_dependency, item: Language, user: user_dependency):
    """
           Додає нову мову до бібліотеки.

           Args:
               item (Language): Об'єкт валідації мови.

           Returns:
               new_language : Створена нова мова
           """
    user_id = user[1]
    new_language = Languages(user_id=user_id,name=item.name)
    db_session.add(new_language)
    db_session.commit()
    return new_language

# Ендпоінт для оновлення мови
@library_router.put('/update_language')
async def update_language(language_id, item: Language, db_session: db_dependency, user: user_dependency):
    """
              Оновлює мову в бібліотеці.

              Args:
                  item (Language): Об'єкт валідації мови.
                  language_id (int): індетифікатор мови

              Returns:
                  language : Оновлена мова
              """
    user_id = user[1]
    user = db_session.query(Users).filter(Users.id == user_id).first()
    language = db_session.query(Languages).filter(Languages.id == language_id).first()
    if not language:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such language')
    if language.user_id == user_id or user.is_admin > 0:
        language.name = item.name
        db_session.commit()
        return language
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail='You are a teapot')

# Ендпоінт для видалення мови
@library_router.delete('/delete_language')
async def delete_language(language_id, db_session: db_dependency, user: user_dependency):
    """
               Видаляє мову з бібліотеки.

               Args:
                  language_id (int): індетифікатор мови

               Returns:
                  language : Видалена мова
               """
    user_id = user[1]
    user = db_session.query(Users).filter(Users.id == user_id).first()
    language = db_session.query(Languages).filter(Languages.id == language_id).first()
    if not language:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such language')
    if language.user_id == user_id or user.is_admin > 0:
        db_session.query(Languages).filter(Languages.id == language_id).delete()
        db_session.commit()
        return language
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail='You are a teapot')

# Ендпоінт для отримання всіх жанрів
@library_router.get('/get_all_genres')
def get_genres(db_session: db_dependency):
    """
           Отримує список всіх жанрів у бібліотеці.

           Returns:
               genres: Список об'єктів жанрів.
           """
    genres = db_session.query(Genres).all()
    return genres

# Ендпоінт для отримання всіх авторів
@library_router.get('/get_all_authors')
def get_authors(db_session: db_dependency):
    """
           Отримує список всіх авторів у бібліотеці.

           Returns:
               authors: Список об'єктів авторів.
           """
    authors = db_session.query(Authors).all()
    return authors

# Ендпоінт для отримання всіх мов
@library_router.get('/get_all_languages')
def get_languages(db_session: db_dependency):
    """
           Отримує список всіх мов у бібліотеці.

           Returns:
               languages: Список об'єктів мов.
           """
    languages = db_session.query(Languages).all()
    return languages

@library_router.post('/create_book-location')
async def create_location(db_session: db_dependency, item: BookLocation, user: user_dependency, book_id):
    """
             Створення розміщення для книги.
             Args:
                  book_id (int): індетифікатор книги
                  item (BookLocation) : об'єкт валідації локації
             Returns:
                 new_location: нова локація.
             """

    user_id = user[1]
    book = db_session.query(Books).filter(Books.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such book')
    new_location = BookLocations(book_id=book_id, location=item.location)
    book.book_location = item.location
    db_session.add(new_location)
    db_session.commit()
    return new_location

@library_router.put('/update_book-location')
async def update_location(id, book_id, item: BookLocation, db_session: db_dependency, user: user_dependency):
    """
                 Оновлює розміщення книги в бібліотеці.

                 Args:
                     item (BookLocation) : об'єкт валідації локації
                     book_id (int): індетифікатор книги
                     id (int): індетифікатор локації

                 Returns:
                     location : Оновлена локація
                 """
    user_id = user[1]
    book = db_session.query(Books).filter(Books.id == book_id).first()
    location = db_session.query(BookLocations).filter(BookLocations.id == id).first()
    user = db_session.query(Users).filter(Users.id == user_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such book')

    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such location')

    if location.book_id != book.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such location for book')

    if location.user_id == user_id or user.is_admin > 0:
        location.location = item.location
        db_session.commit()
        return location
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail='You are a teapot')

# Ендпоінт для отримання фізичного положення книги
@library_router.get("/books/{book_id}/location")
def get_book_location(book_id: int, db=Depends(get_session)):
    """
       Отримує інформацію про фізичне положення заданої книги.

       Args:
           book_id (int): Ідентифікатор книги.

       Returns:
           book_location: Об'єкт фізичного положення книги або код 404, якщо не знайдено.
       """
    book_location = (
        db.query(BookLocations)
        .filter(BookLocations.book_id == book_id)
        .order_by(BookLocations.timestamp.desc())
        .first()
    )

    if not book_location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found location")

    return book_location

# Ендпоінт створення історії користувача
@library_router.post('/create_user-history')
async def create_history(db_session: db_dependency, item: UserHistory, user: user_dependency):
    """
    Створення історії користувача.
    Args:
        item (UserHistory): об'єкт валідації історії користувача
    Returns:
        new_user_history: нова історія користувача.
    """
    user_id = user[1]
    new_user_history = UserHistories(user_id=user_id, action=item.action, timestamp=datetime.utcnow())
    user = db_session.query(Users).filter(Users.id == user_id).first()
    user.actions = item.action
    db_session.add(new_user_history)
    db_session.commit()
    return new_user_history

# Ендпоінт для отримання історії користування бібліотекою в розрізі користувача
@library_router.get("/users/{user_id}/library-history")
def get_user_library_history(user_id: int,db=Depends(get_session)):
    """
       Отримує історію користування бібліотекою для заданого користувача.

       Args:
           user_id (int): Ідентифікатор користувача.

       Returns:
           user_history: Список об'єктів історії користування бібліотекою або код 404, якщо не знайдено.
       """
    user_history = db.query(UserHistories).filter(UserHistories.user_id == user_id).all()

    if not user_history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found history for this user")

    return user_history

# Ендпоінт створення історії книги
@library_router.post('/create_book-history')
async def create_book_history(db_session: db_dependency, item: BookHistory, user: user_dependency):
    """
    Створення історії користувача.
    Args:
        item (BookHistory): об'єкт валідації історії книги
    Returns:
        new_book_history: нова історія книги.
    """
    user_id = user[1]
    new_book_history = BookHistories(book_id=item.book_id,user_id=user_id,checked_out=datetime.utcnow(),checked_in=datetime.utcnow())

    db_session.add(new_book_history)
    db_session.commit()

    return new_book_history


# Ендпоінт для отримання історії користування бібліотекою в розрізі книги
@library_router.get("/books/{book_id}/library-history")
def get_book_library_history(book_id: int, db=Depends(get_session)):
    """
       Отримує історію користування бібліотекою для заданої книги.

       Args:
           book_id (int): Ідентифікатор книги.

       Returns:
           book_history: Список об'єктів історії користування бібліотекою або код 404, якщо не знайдено.
       """
    book_history = (
        db.query(UserHistory)
        .join(BookHistory)
        .filter(BookHistory.book_id == book_id)
        .all()
    )

    if not book_history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found history for this book")

    return book_history

