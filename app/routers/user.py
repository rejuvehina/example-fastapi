from .. import models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from ..database import get_db

router = APIRouter(prefix= "/users", tags=["users"])

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserOut)
async def user_create(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model= schemas.UserOut)
async def get_user_profile(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no such user!")
    else:
        return user