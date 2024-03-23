from data.db import engine, Base

from models.model import User
from models.model import Book
from models.model import BookDetails
from models.model import BorrowedBook
from models.user import SecurityUser


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
