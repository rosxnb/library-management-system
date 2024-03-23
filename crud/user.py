from sqlalchemy.orm import Session
from schemas.user import UserInDB
from models.user import SecurityUser


def get_user(session: Session, username: str) -> SecurityUser:
    query = session.query(SecurityUser).filter_by(user_name=username)
    return query.first()


def insert_user(session: Session, user: UserInDB) -> SecurityUser:
    new_user = SecurityUser(
        user_name = user.username,
        email = user.email,
        full_name = user.full_name,
        hashed_password = user.hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

