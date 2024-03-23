from pydantic import BaseModel


class BookDetailsBase(BaseModel):
    no_of_pages: int = 0
    publisher: str = "unknown"
    language: str | None = None


class BookDetailsCreate(BookDetailsBase):
    pass


class BookDetailsReturn(BookDetailsCreate):
    details_id: int


class BookDetailsSchema(BookDetailsReturn):
    book_id: int

    class config:
        from_attributes = True
