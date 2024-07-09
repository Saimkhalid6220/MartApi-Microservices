from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from sqlmodel import SQLModel, Session , create_engine
from userservice import setting


connectionString = str(setting.DATABASE_URL).replace(
    "postgresql" , "postgresql+psycopg"
)

engine = create_engine(connectionString , connect_args={})

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app:FastAPI)->AsyncGenerator[None , None]:
    print("hooray  creating tables")
    create_db_and_table()
    yield

def getSession():
    with Session(engine) as session:
        yield session