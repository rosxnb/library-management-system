from fastapi import APIRouter, HTTPException, status, Depends
from crud import crud_user as crud
from schemas.user import UserCreate, UserSchema, UserReturn
from schemas.responses import Response404, Response500, Response400, Response406
from security.security import oauth2_scheme
from .dependencies import MySqlDB


router = APIRouter(
    prefix = "/users",
    tags = ["users"],
    dependencies = [Depends(oauth2_scheme)],
)


# List all users
@router.get(
    "/",
    responses={
        500: {"model": Response500},
    },
    response_model=list[UserSchema],
    status_code=status.HTTP_200_OK,
)
def get_users(
    db: MySqlDB,
    skip: int = 0,
    limit: int = 100,
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# Create new user
@router.post(
    "/create",
    responses={
        400: {"model": Response400},
        500: {"model": Response500},
    },
    response_model=UserReturn,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    db: MySqlDB,
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


# Get user by user_id
@router.get(
    "/{user_id}",
    responses={
        404: {"model": Response404},
        406: {"model": Response406},
        500: {"model": Response500},
    },
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
def get_user_by_id(
    user_id: int,
    db: MySqlDB,
):
    if user_id == 0:
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Uacceptable ID 0",
        )

    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user
