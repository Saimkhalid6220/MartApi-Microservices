from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from userservice.db import getSession
from userservice.models import Password, Update_password_request, Update_request, Updated, User
from userservice.routers.auth import get_current_user

router = APIRouter(
    tags=['Manage Profile'],
    dependencies=[Depends(get_current_user)]
)

@router.get('/profile',response_model=User)
async def get_profile(password:str , current_user:Annotated[User,Depends(get_current_user)],session:Annotated[Session,Depends(getSession)]):
    if password==current_user.password:
        return current_user
    raise HTTPException(
        status_code=401,
        detail={"message" : "unauthorised to perform action"}
    )

@router.patch('/profile',response_model=Updated)
async def update_profile(user:Update_request,current_user:Annotated[User,Depends(get_current_user)],session:Annotated[Session,Depends(getSession)])->Updated:
    if user.old_password==current_user.password:
        update_user = user.model_dump(exclude_unset=True)
        current_user.sqlmodel_update(update_user)
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return Updated(email=user.email)
    raise HTTPException(
        status_code=401,
        detail={"message" : "unauthorised to perform action"}
    )

@router.patch('/profile/password',response_model=Update_password_request)
async def update_password(user:Update_password_request,current_user:Annotated[User,Depends(get_current_user)],session:Annotated[Session,Depends(getSession)])->Update_password_request:
    if user.old_password==current_user.password:
        update_pass=Password(password=user.new_password)
        update_user = update_pass.model_dump(exclude_unset=True)
        current_user.sqlmodel_update(update_user)
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return user
    raise HTTPException(
        status_code=401,
        detail={"message" : "unauthorised to perform action"}
    )

@router.delete('/profile' )
async def delete_user(password:str,current_user:Annotated[User,Depends(get_current_user)],session:Annotated[Session,Depends(getSession)]):
    if password==current_user.password:
        session.delete(current_user)
        session.commit()
        return {"message" : "user has deleted"}
    raise HTTPException(
        status_code=401,
        detail={"message" : "unauthorised to perform action"}
    )