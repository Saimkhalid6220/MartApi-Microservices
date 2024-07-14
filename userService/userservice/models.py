from typing import Optional
from fastapi import Form
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email:str = Field(index=True)
    password:str = Field()

class TokenData(SQLModel):
    email: str | None = None

class Token(SQLModel):
    access_token: str
    token_type: str


class Update_user(SQLModel):
    id: Optional[int]
    email:str 
    password:str 

class Forgot_password_request(SQLModel):
    email:str

class Forgot_password(SQLModel):
    reset_token:str
    new_password:str

class Update_request(SQLModel):
    email:str
    old_password:str

class Updated(SQLModel):
    email:str

class Update_password_request(SQLModel):
    old_password:str
    new_password:str

class Password(SQLModel):
    password:str   