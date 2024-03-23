from data.create_tables import create_tables
create_tables()

from fastapi import FastAPI

from routers import user
from routers import book
from routers import borrow_book
from routers import login


server = FastAPI()
server.include_router(login.router)
server.include_router(user.router)
server.include_router(book.router)
server.include_router(borrow_book.router)


@server.get("/")
async def home():
    return { "message": "Library Management System" }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         server,
#         host="127.0.0.1", 
#         port=8000,
#     )

