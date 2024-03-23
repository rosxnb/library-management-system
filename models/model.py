from sqlalchemy import ForeignKey, String, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from data.db import Base


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    email: Mapped[str | None] = mapped_column(String(100))
    membership_date: Mapped[date] = mapped_column(String(15))

    books_borrowed: Mapped[list["BorrowedBook"]] = relationship("BorrowedBook", back_populates="user")


class Book(Base):
    __tablename__ = "book"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    isbn: Mapped[str] = mapped_column(String(50))
    publish_date: Mapped[date] = mapped_column(String(15))
    genre: Mapped[str | None] = mapped_column(String(100))

    details: Mapped["BookDetails"] = relationship("BookDetails", back_populates="book_data", uselist=False)


class BookDetails(Base):
    __tablename__ = "book_details"

    details_id: Mapped[int] = mapped_column(primary_key=True)
    no_of_pages: Mapped[int] = mapped_column(Integer)
    publisher: Mapped[str] = mapped_column(String(100))
    language: Mapped[str | None] = mapped_column(String(100))

    book_id = mapped_column(ForeignKey("book.book_id"))

    book_data: Mapped[Book] = relationship("Book", back_populates="details", single_parent=True)

    __table_args__ = (UniqueConstraint("book_id"), )


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[int] = mapped_column(primary_key=True)
    borrow_date: Mapped[date] = mapped_column(String(15))
    return_date: Mapped[date] = mapped_column(String(15))

    user_id = mapped_column(ForeignKey("user.user_id"))
    book_id = mapped_column(ForeignKey("book.book_id"))

    user: Mapped[User] = relationship(back_populates="books_borrowed")
