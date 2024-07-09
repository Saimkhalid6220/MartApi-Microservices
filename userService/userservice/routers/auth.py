from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from sqlmodel import Session, select
from userservice.models import Token, TokenData, User
from userservice.main import getSession

router=APIRouter(
    prefix='/user',
    tags=['Auth'],
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt          

def authenticate_user(user:User , Vuser , Vpassword):
    if not user.username==Vuser and user.password==Vpassword:
        raise HTTPException(status_code=401 , details="invaild credientials")
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],session:Annotated[Session,Depends(getSession)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    user:User = session.exec(select(User).filter(User.username==token_data.username)).first()
    if user is None:
        raise credentials_exception
    return user

@router.post('/register' , response_model=User)
async def register_user(user:User  ,session : Annotated[Session , Depends(getSession)]):
    if not session.exec(select(User).filter(User.username==user.username)).first():
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    raise HTTPException(status_code=409,detail="user already exist")

@router.post('/login' , response_model=Token)
async def login_user(session:Annotated[Session , Depends(getSession)],form_data: Annotated[OAuth2PasswordRequestForm, Depends()])->Token:   
    # user = session.get(User,id)
    is_user:User = session.exec(select(User).filter(User.username==form_data.username)).first()
    user = authenticate_user(form_data,is_user.username , is_user.password)
    if not user or not is_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

