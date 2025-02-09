# A Simplified Setup for FastAPI and SQLModel


## Why?

Because this:
```python
@app.get("/users/create")
async def users_create() -> User:
    user = User.create("Blank User")
    return user
```

Is much nicer than this:

```python
@app.get("/users/create/")
def create_hero(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
```


This takes the SQLModel integration from the [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/) and simplifies it down to a static DB class that can be used anywhere, without passing in the session as a dependency.  
Instead of passing the DB session as a dependency for every route, you just need to call `DB.init()` at some point, either on startup or within your route logic. Then you can access the static `DB.session` variable whenever you need to work with the DB, wheather its directly or via a Model class (like `User` in this demo)

```python
# index.py

from fastapi import FastAPI
from database import DB
from user import User

app = FastAPI()

@app.on_event("startup")
def on_startup():
    DB.init() # This is where the DB setup happens


@app.get("/users/create")
async def users_create():
    user = User.create("Blank User")
    return user
```

You could also call `DB.init()` from within your route if you don't need to have it initiated by default:

```python
@app.get("/users")
async def users():
    DB.init() # Setup the DB here instead

    users = User.get_all()
    return users
```


```python
# user.py

from sqlmodel import Field, SQLModel, select
from database import DB


class UserModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)


"""
    Wrapper class for the UserModel. This is where the DB interactions occur.
"""
class User(UserModel):
    def create(name) -> UserModel:
        user = UserModel(name=name)
        DB.session.add(user)
        DB.session.commit()
        DB.session.refresh(user)
        return user

    def get_all() -> list[UserModel]:
        users = DB.session.exec(select(UserModel)).all()
        return users
    
```


```python
# database.py

from sqlmodel import Session, SQLModel, create_engine

class DB:    
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)
    session: Session = None

    @staticmethod
    def create_db_and_tables():
        # This logic can be replaced with your migration handler
        SQLModel.metadata.create_all(DB.engine)

    @staticmethod
    def get_session():
        # Returns the existing DB session or create a new one.

        if DB.session:
            return DB.session
        
        with Session(DB.engine) as session:
            return session

    @staticmethod 
    def init():
        DB.create_db_and_tables()
        DB.session = DB.get_session()

```


## Running the demo
Clone this repo, and then install the pip dependencies.  
```pip install -r requirements.txt```  

Then run the dev server  
```fastapi dev index.py```  

After the server is started, you can navigate to `/users/` and `/users/create` to view/create demo users.
