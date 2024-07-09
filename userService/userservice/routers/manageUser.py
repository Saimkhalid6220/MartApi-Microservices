from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from userservice.db import getSession
from userservice.models import Update_user, User
from userservice.routers.auth import get_current_user

router = APIRouter(
    tags=['Manage Profile'],
    dependencies=[Depends(get_current_user)]
)

@router.get('/user',response_model=User)
async def get_user(current_user:Annotated[User,Depends(get_current_user)]):
    return current_user

@router.patch('/user',response_model=User)
async def update_user(user:User,current_user:Annotated[User,Depends(get_current_user)],session:Annotated[Session,Depends(getSession)])->Update_user:
    update_user = user.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(update_user)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@router.delete('/user' )
async def delete_user(current_user:Annotated[User,Depends(get_current_user)],session:Annotated[Session,Depends(getSession)]):
    session.delete(current_user)
    session.commit()
    return {"message" : "user has deleted"}