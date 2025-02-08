from sqlmodel import Field, SQLModel, select
from database import DB


class UserModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)


"""
    Wrapper class for the UserModel.
    This is where the DB interactions occur
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
    