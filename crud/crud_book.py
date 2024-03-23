from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models.model import Book
from models.model import BookDetails
from schemas.book import BookCreate
from schemas.book_details import BookDetailsCreate


def get_book(db: Session, book_id: int) -> Book:
    filter_query = db.query(Book).filter(Book.book_id == book_id)
    join_query = filter_query.options(joinedload(Book.details))
    return join_query.first()


def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[Book]:
    filter_query = db.query(Book).offset(skip).limit(limit)
    join_query = filter_query.options(joinedload(Book.details))
    return join_query.all()


def store_book(db: Session, book: BookCreate) -> Book:
    # Create Book
    db_book = db.query(Book).filter(Book.title == book.title).first()
    if db_book:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Book with title: '{book.title}' already exists"
        )

    db_book = Book(title=book.title, isbn=book.isbn, publish_date=book.publish_date, genre=book.genre)
    book_detail = BookDetails(
        no_of_pages=book.details.no_of_pages,
        publisher=book.details.publisher,
        language=book.details.language
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    book_detail.book_id = db_book.book_id
    db.add(book_detail)
    db.commit()
    db.refresh(book_detail)
    return db_book


def update_book(db: Session, book_id: int, details: BookDetailsCreate) -> str:
    book = db.query(Book).filter(Book.book_id == book_id).first()

    if not book:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No book with id: {book_id}"
        )

    book.details.no_of_pages = details.no_of_pages
    book.details.publisher = details.publisher
    book.details.language = details.language

    db.commit()
