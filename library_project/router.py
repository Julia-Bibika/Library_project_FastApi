import dotenv
import psycopg2
from fastapi import APIRouter,Depends

from models import Books, Authors, Genres, Languages
from pydantic_models import Book, Author, Genre, Language
from session import get_session

router = APIRouter()

dotenv.load_dotenv(".env")
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

@router.post("/create_book")
async def add_book(book: Book,db=Depends(get_session)):
    db.add(Books(name=book.name, author=book.author,genre = book.genre,language = book.language))
    db.commit()

    return db.query(Books).all()

@router.post("/create_author")
async def add_author(author: Author, db=Depends(get_session)):
    db.add(Authors(name=author.name))
    db.commit()

    return db.query(Authors).all()

@router.post("/create_genre")
async def add_genre(genre: Genre, db=Depends(get_session)):
    db.add(Genres(name=genre.name))
    db.commit()

    return db.query(Genres).all()
@router.post("/create_language")
async def add_genre(language: Language, db=Depends(get_session)):
    db.add(Languages(name=language.name))
    db.commit()

    return db.query(Languages).all()
