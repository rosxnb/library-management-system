from pydantic import BaseModel
from datetime import date

from .borrow_books import BorrowBookSchema


class UserBase(BaseModel):
    name: str
    email: str | None = None
    membership_date: date


class UserCreate(UserBase):
    pass


class UserReturn(UserCreate):
    user_id: int


class UserSchema(UserReturn):
    books_borrowed: list[BorrowBookSchema]

    class config:
        from_attributes = True


class BaseUser(BaseModel):
    username: str
    email: str
    full_name: str


class InputModelUser(BaseUser):
    password: str


class ResponseModelUser(BaseUser):
    pass


class UserInDB(BaseUser):
    hashed_password: str
