from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from sqlmodel import Session, select
from userservice.models import Token, TokenData, User
from userservice.db import getSession
from userservice.setting  import SECRET_KEY,ALGORITHM

router=APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt          

def authenticate_user(user,Vuser,Vpassword):
    if not (user.username==Vuser and user.password==Vpassword):
        raise HTTPException(status_code=401 , detail="invaild credientials")
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],session:Annotated[Session,Depends(getSession)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.InvalidTokenError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    user:User = session.exec(select(User).filter(User.email==token_data.email)).first()
    if user is None:
        raise credentials_exception
    return user

@router.post('/register' , response_model=User)
async def register_user(user:User  ,session : Annotated[Session , Depends(getSession)]):
    if not session.exec(select(User).filter(User.email==user.email)).first():
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    raise HTTPException(status_code=409,detail="user already exist")

@router.post('/login' ,response_model=Token)
async def login_user(session:Annotated[Session , Depends(getSession)],form_data: Annotated[OAuth2PasswordRequestForm, Depends()])->Token:   
    # user = session.get(User,id)
    isUser = session.exec(select(User).filter(User.email==form_data.username)).first()
    user = authenticate_user(form_data,isUser.email,isUser.password)
    if not user or not isUser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
