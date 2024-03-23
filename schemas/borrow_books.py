from pydantic import BaseModel
from datetime import date


class BorrowBookBase(BaseModel):
    book_id: int


class BorrowBookCreate(BorrowBookBase):
    borrow_date: date
    return_date: date


class BorrowBookSchema(BorrowBookCreate):
    id: int
    user_id: int

    class config:
        from_attributes = True
