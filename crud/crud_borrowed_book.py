from sqlalchemy.orm import Session
from models.model import BorrowedBook, User
from schemas.borrow_books import BorrowBookCreate
from fastapi import HTTPException, status


def get_borrow_list(db: Session, skip: int = 0, limit: int = 100) -> list[BorrowedBook]:
    return db.query(BorrowedBook).offset(skip).limit(limit).all()


def return_borrowed_book(db: Session, id: int) -> None:
    query = db.query(BorrowedBook).filter(BorrowedBook.id == id)
    
    if not query.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No record of borrowed id: {id}"
        )

    query.delete()
    db.commit()


def borrow_book(db: Session, user_id: int, data: BorrowBookCreate) -> BorrowedBook:
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No record of user id: {user_id}"
        )

    borrow_info = BorrowedBook(
        user_id = user_id,
        book_id = data.book_id,
        borrow_date = data.borrow_date,
        return_date = data.return_date
    )
    db.add(borrow_info)
    db.commit()
    db.refresh(borrow_info)
    return borrow_info
