from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import Response
from crud import crud_borrowed_book as crud
from schemas.borrow_books import BorrowBookCreate, BorrowBookSchema
from schemas.responses import Response404, Response500, Response406
from security.security import oauth2_scheme
from .dependencies import MySqlDB


router = APIRouter(
    tags = ["borrow"],
    dependencies = [Depends(oauth2_scheme)],
)


# List all books
@router.get(
    "/borrow-list/",
    responses={
        500: {"model": Response500},
    },
    status_code=status.HTTP_200_OK,
    response_model=list[BorrowBookSchema],
)
def get_borrowed_list(
    db: MySqlDB,
    skip: int = 0,
    limit: int = 100,
):
    users = crud.get_borrow_list(db, skip=skip, limit=limit)
    return users


# Borrow new book
@router.put(
    "/users/{user_id}/borrow",
    responses={
        404: {"model": Response404},
        406: {"model": Response406},
        500: {"model": Response500},
    },
    status_code=status.HTTP_201_CREATED,
    response_model=BorrowBookSchema,
)
def borrow_book(
    db: MySqlDB,
    book_data: BorrowBookCreate,
    user_id: int,
):
    if book_data.book_id == 0 or user_id == 0:
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Uacceptable ID 0",
        )

    return crud.borrow_book(db=db, user_id=user_id, data=book_data)


# Return a borrowed book
@router.delete(
    "/borrow-return/{id}",
    responses={
        404: {"model": Response404},
        406: {"model": Response406},
        500: {"model": Response500},
    },
    status_code = status.HTTP_204_NO_CONTENT,
    response_class = Response,
)
def return_borrowed_book(
    id: int,
    db: MySqlDB,
):
    if id == 0:
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Uacceptable ID 0",
        )

    crud.return_borrowed_book(db, id=id)
