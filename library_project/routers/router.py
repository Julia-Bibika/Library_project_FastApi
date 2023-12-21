import dotenv
import psycopg2
from fastapi import APIRouter, Depends, HTTPException

from models import Book, Author, Genre, Language, BookLocation, UserHistory, BookHistory
from pydantic_models import BookValidation, AuthorValidation, GenreValidation, LanguageValidation
from session import get_session

router = APIRouter()

dotenv.load_dotenv("../.env")
conn_dict = {
    "host": "localhost",
    "user": "postgres",
    "password": "21345",
    "port": 5432,
    "database":"for_library",
}

connection = psycopg2.connect(
    **conn_dict
)
# Ендпоінт для отримання всіх книг
@router.get("/books")
def get_all_books(db=Depends(get_session)):
    """
       Отримує список всіх книг у бібліотеці.

       Returns:
           books: Список об'єктів книг.
       """
    books = db.query(Book).all()
    return books

# Ендпоінт для отримання фізичного положення книги
@router.get("/books/{book_id}/location")
def get_book_location(book_id: int, db=Depends(get_session)):
    """
       Отримує інформацію про фізичне положення заданої книги.

       Args:
           book_id (int): Ідентифікатор книги.

       Returns:
           book_location: Об'єкт фізичного положення книги або код 404, якщо не знайдено.
       """
    book_location = (
        db.query(BookLocation)
        .filter(BookLocation.book_id == book_id)
        .order_by(BookLocation.timestamp.desc())
        .first()
    )

    if not book_location:
        raise HTTPException(status_code=404, detail="Фізичне положення книги не знайдено")

    return book_location

# Ендпоінт для отримання історії користування бібліотекою в розрізі користувача
@router.get("/users/{user_id}/library-history")
def get_user_library_history(user_id: int,db=Depends(get_session)):
    """
       Отримує історію користування бібліотекою для заданого користувача.

       Args:
           user_id (int): Ідентифікатор користувача.

       Returns:
           user_history: Список об'єктів історії користування бібліотекою або код 404, якщо не знайдено.
       """
    user_history = db.query(UserHistory).filter(UserHistory.user_id == user_id).all()

    if not user_history:
        raise HTTPException(status_code=404, detail="Історія користування бібліотекою для цього користувача не знайдена")

    return user_history

# Ендпоінт для отримання історії користування бібліотекою в розрізі книги
@router.get("/books/{book_id}/library-history")
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
        raise HTTPException(status_code=404, detail="Історія користування бібліотекою для цієї книги не знайдена")

    return book_history

# Ендпоінт для додавання нової книги
@router.post("/create_book")
async def add_book(book: BookValidation,db=Depends(get_session)):
    """
       Додає нову книгу до бібліотеки.

       Args:
           book (BookValidation): Об'єкт валідації книги.

       Returns:
           List[Book]: Список всіх книг після додавання нової.
       """
    db.add(Book(name=book.name, author_id=book.author_id,genre_id = book.genre_id,language_id = book.language_id))
    db.commit()

    return db.query(Book).all()

# Ендпоінт для додавання нового автора
@router.post("/create_author")
async def add_author(author: AuthorValidation, db=Depends(get_session)):
    """
     Додає нового автора до бібліотеки.

     Args:
         author (AuthorValidation): Об'єкт валідації автора.

     Returns:
         List[Author]: Список всіх авторів після додавання нового.
     """
    db.add(Author(name=author.name))
    db.commit()

    return db.query(Author).all()

# Ендпоінт для додавання нового жанру
@router.post("/create_genre")
async def add_genre(genre: GenreValidation, db=Depends(get_session)):
    """
       Додає новий жанр до бібліотеки.

       Args:
           genre (GenreValidation): Об'єкт валідації жанру.

       Returns:
           List[Genre]: Список всіх жанрів після додавання нового.
       """
    db.add(Genre(name=genre.name))
    db.commit()

    return db.query(Genre).all()

# Ендпоінт для додавання нової мови
@router.post("/create_language")
async def add_genre(language: LanguageValidation, db=Depends(get_session)):
    """
          Додає нову мову до бібліотеки.

          Args:
              language (LanguageValidation): Об'єкт валідації мови.

          Returns:
              List[Language]: Список всіх мов після додавання нової.
          """
    db.add(Language(name=language.name))
    db.commit()

    return db.query(Language).all()
# Ендпоінт для оновлення книги
@router.put("/update_book/{book_id}")
async def update_book(book_id: int, book_data: BookValidation, db=Depends(get_session)):
    """
             Оновлює інформацію про книгу в бібліотеці.

             Args:
                book_id (int): Ідентифікатор книги.
                book_data (BookValidation): Об'єкт валідації для оновлення.

             Returns:
                  Book: Оновлений об'єкт книги абокод 404, якщо книга не знайдена.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        for field, value in book_data.dict().items():
            setattr(db_book, field, value)
        db.commit()
        db.refresh(db_book)
        db.close()
        return db_book
    else:
        raise HTTPException(status_code=404, detail="Книга не знайдена")