from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from data.db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


MySqlDB = Annotated[
    Session,
    Depends(get_db)
]
