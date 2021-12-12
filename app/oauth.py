from fastapi.param_functions import Depends
from jose import JWSError,jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session

from app import models
from app.config import Settings
from . import orm


oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = Settings.database_secret_key
ALGORITHM = Settings.database_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = Settings.database_expire_time

def myconverter(o):#lookup this later
    if isinstance(o,datetime):
        return o.__str__()

def token_generate(data:dict):
    playing_data=data.copy()
    expire_time=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_time=myconverter(expire_time)
    playing_data.update({'expire_time':expire_time})
    generated_token=jwt.encode(playing_data,SECRET_KEY,algorithm=ALGORITHM)
    return generated_token

def verify_token(token:str,credentials_exception):
    try:
        decode_token=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        idofuser:str=decode_token.get('user_id')
        if not idofuser:
            raise credentials_exception
    except JWSError:
        raise credentials_exception

    return idofuser

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(orm.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"invalid credentials",
    headers={"WWW-Authenticate": "Bearer"})
    user_id=verify_token(token,credentials_exception)
    print(user_id)
    username=db.query(models.user).filter(models.user.id==user_id).first()
    print(username)
    return username
    
    




