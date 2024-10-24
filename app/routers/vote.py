from typing import List, Optional
from .. import models, schemas, oauth2, database
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from ..database import get_db

router = APIRouter(prefix= "/votes", tags=["Votes"])

@router.post("/", status_code= status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session= Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    fetched = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).first()

    if not fetched:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "The Post id is not correct!")
    
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"User with id of {current_user.id} has already voted!")
        new_vote = models.Vote(post_id= vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully vote!"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Either post is incorrect or user is not correct!")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully revoke the vote!"}
    