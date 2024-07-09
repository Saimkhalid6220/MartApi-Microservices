from typing import Optional
from sqlmodel import Field, SQLModel


class TokenData(SQLModel):
    username: str | None = None

class Token(SQLModel):
    access_token: str
    token_type: str

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username:str = Field(index=True)
    password:str = Field()

class Update_user(SQLModel):
    id: Optional[int]
    username:str 
    password:str 