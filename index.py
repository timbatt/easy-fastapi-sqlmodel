from fastapi import FastAPI
from database import DB

from user import User

app = FastAPI()


@app.on_event("startup")
def on_startup():
    DB.init()

@app.get("/")
async def index():
    return {"message": "Sup homies"}


@app.get("/users/create")
async def users_create():
    user = User.create("Blank User")
    return user


@app.get("/users")
async def users():
    users = User.get_all()
    return users