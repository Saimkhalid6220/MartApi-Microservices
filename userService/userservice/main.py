from userservice.db import lifespan
from userservice.routers import auth, managePassword, manageUser
from fastapi import FastAPI



app = FastAPI(
    title='User Service',
    version='1.0.0',
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(manageUser.router)
app.include_router(managePassword.router)


