from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI,Depends
from sqlmodel import Session
from userservice.models import User
from userservice.db import getSession
from userservice.routers import auth, manageUser
from userservice.routers.auth import get_current_user

app = FastAPI(
    title='User Service',
    version='1.0.0'
)

app.include_router(auth.router)
app.include_router(manageUser.router)


