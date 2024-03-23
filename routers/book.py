from fastapi import APIRouter, HTTPException, status, Depends
from schemas.book import BookCreate, BookReturn
from schemas.book_details import BookDetailsCreate
from schemas.responses import Response404, Response500, Response400, Response406
from crud import crud_book as crud
from models.model import Book
from .dependencies import MySqlDB
from security.security import oauth2_scheme


router = APIRouter(
    prefix = "/books",
    tags = ["books"],
    dependencies = [Depends(oauth2_scheme)],
)


# List all books
@router.get(
    "/", 
    responses={
        500: {"model": Response500},
    },
    status_code=status.HTTP_200_OK,
    response_model=list[BookReturn],
)
def list_all_books(
    db: MySqlDB,
    skip: int = 0,
    limit: int = 100,
):
    books: list[Book] = crud.get_books(db, skip=skip, limit=limit)
    return books


# Store new book
@router.post(
    "/store", 
    responses={
        400: {"model": Response400},
        500: {"model": Response500},
    },
    status_code=status.HTTP_201_CREATED,
    response_model=BookReturn,
)
def record_new_book(
    book: BookCreate,
    db: MySqlDB,
):
    return crud.store_book(db=db, book=book)


# Get book by book_id
@router.get(
    "/{book_id}", 
    responses={
        404: {"model": Response404},
        406: {"model": Response406},
        500: {"model": Response500},
    },
    status_code=status.HTTP_200_OK,
    response_model=BookReturn,
)
def retreive_book_by_id(
    book_id: int,
    db: MySqlDB,
):
    if book_id == 0:
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Uacceptable ID 0",
        )

    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


# Update book details by book_id
@router.put(
    "/update/{book_id}", 
    responses={
        404: {"model": Response404},
        406: {"model": Response406},
        500: {"model": Response500},
    },
    status_code=status.HTTP_201_CREATED,
    response_model=BookReturn,
)
def update_book_details(
    book_id: int,
    db: MySqlDB,
    details: BookDetailsCreate
):
    if book_id == 0:
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Uacceptable ID 0",
        )
    
    crud.update_book(db, book_id=book_id, details=details)

    return crud.get_book(db, book_id=book_id)
