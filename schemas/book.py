from pydantic import BaseModel
from datetime import date

from .book_details import BookDetailsCreate, BookDetailsReturn


class BookBase(BaseModel):
    title: str
    isbn: str
    publish_date: date
    genre: str | None = None


class BookUpdate(BookBase):
    details: BookDetailsCreate


class BookCreate(BookUpdate):
    pass


class BookSchema(BookUpdate):
    book_id: int

    class config:
        from_attributes = True


class BookReturn(BookBase):
    book_id: int
    details: BookDetailsReturn
