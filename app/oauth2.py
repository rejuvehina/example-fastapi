from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from .config import settings

oauth_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithmn
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(payload:dict):
    orignal_payload = payload.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    orignal_payload.update({"exp": expire})
    encoded = jwt.encode(orignal_payload, SECRET_KEY, ALGORITHM)
    return encoded

def verify_access_token(token: str, crediential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise crediential_exception
        token_data = schemas.TokenData(id=id)
        print(token_data)
    except Exception as e:
        print(e)
        raise crediential_exception
    print(token_data)
    return token_data # why we return a token instance instead of ID?

def get_current_user(token: str = Depends(oauth_schema)):
    crediential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validaite the credentials.", headers = {"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, crediential_exception)