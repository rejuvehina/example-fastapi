from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db

router = APIRouter(prefix= "/login", tags=["Authentication"])

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Token)
#By not passing any argument to Depends(), FastAPI will use OAuth2PasswordRequestForm as the default dependency resolver. 
# his implies that FastAPI will instantiate OAuth2PasswordRequestForm using the request data and inject it into the login function as user_credentials.
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!")
    token = oauth2.create_access_token(payload={"user_id": user.id})
    return{"token": token, "token_type": "bearer"}   