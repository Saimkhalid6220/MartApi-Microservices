from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
import jwt
from sqlmodel import Session, select
from userservice.db import getSession
from userservice.models import Forgot_password, Forgot_password_request, TokenData, User
from userservice.routers.auth import create_access_token
from userservice.setting import ALGORITHM, SECRET_KEY

RECOVERY_TOKEN_EXPIRE_MINUTES = 5


router = APIRouter(
    prefix='/user',
    tags=['Manage password']
)

def send_email(to_email: str, subject: str, body: str):
    from_email:str = "ziamartpi@gmail.com"
    # password:str = "formartapi6221"
    
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("ziamartpi@gmail.com", "jjhv eclk otlh edwi")
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@router.post('/forgot_password')
async def request_password_recovery(session:Annotated[Session,Depends(getSession)] ,req:Forgot_password_request):
    user = session.exec(select(User).filter(User.email==req.email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="email not valid")
    now = datetime.today()
    reset_token_expires = timedelta(minutes=RECOVERY_TOKEN_EXPIRE_MINUTES)
    reset_token = create_access_token(
        data={"sub":user.email,"iat":now} , expires_delta=reset_token_expires
    )
    email_body = f"frontend is not ready but here is your reset_token: {reset_token}"
    if send_email(user.email, "Password Reset", email_body):
        return {"detail": "Password reset token sent"}
    raise HTTPException(status_code=500 , detail="error sending email")

@router.post('/reset_password')
async def reset_password(session:Annotated[Session,Depends(getSession)] ,reset:Forgot_password):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(reset.reset_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.InvalidTokenError:
        raise credentials_exception
    changed_user:User = session.exec(select(User).filter(User.email==token_data.email)).first()
    user:User = session.exec(select(User).filter(User.email==token_data.email)).first()
    user.password = reset.new_password
    update_password = user.model_dump(exclude_unset=True)
    changed_user.sqlmodel_update(update_password)
    session.add(changed_user)
    session.commit()
    return {"message":"password reset successfully"}