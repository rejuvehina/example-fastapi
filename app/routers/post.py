from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from ..database import get_db

router = APIRouter(prefix= "/posts", tags=["posts"])


#@router.get("/", response_model= List[schemas.Post])
@router.get("/") #这个地方怎么试都不对 response model就是不对
async def get_request(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, keyword: Optional[str] = ""):
    #post = db.query(models.Post).filter(models.Post.title.contains(keyword)).limit(limit).offset(skip).all() #db.query(models.Post) 我们传递model, 我们可以get每一个post

    posts = db.query(models.Post, func.count(models.Vote.post_id).\
                    label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).\
                    group_by(models.Post.id).filter(models.Post.title.contains(keyword)).limit(limit).offset(skip).all()
    
    print(posts)

    posts_serialized = [
        {
            "post": {
                "id": post.id,
                "published": post.published,
                "owner_id": post.owner_id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,
                "owner": {
                    "id": post.owner.id,
                    "email": post.owner.email,
                    "created_at": post.owner.created_at
                }
            },
            "votes": votes
        }
        for post, votes in posts
    ]
    
    return posts_serialized


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
async def new_post(para: schemas.CreateUpdate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)): # 这个int真的莫名其妙
    print(user_id)
    row = models.Post(owner_id = user_id.id, **para.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/{id}") #这个地方怎么试都不对 response model就是不对
async def get_individual(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    data = db.query(models.Post, func.count(models.Vote.post_id).\
                    label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).\
                    group_by(models.Post.id).filter(models.Post.id == id).first()
    print(data)
    if data:
        post, votes = data
        data_serialized = {
            "post": {
                "id": post.id,
                "published": post.published,
                "owner_id": post.owner_id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,
                "owner": {
                    "id": post.owner.id,
                    "email": post.owner.email,
                    "created_at": post.owner.created_at
                }
            },
            "votes": votes
        }
        return data_serialized
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "The ID you are searching is not found!")


@router.delete("/{id}")
async def delete(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    fetched = db.query(models.Post).filter(models.Post.id == id)
    if fetched.first():
        if fetched.first().owner_id == user_id.id:
            fetched.delete(synchronize_session=False)
            db.commit()
        else:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You are not authorized to delete this post!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "The ID you are searching is not found!")


@router.put("/{id}",response_model= schemas.Post)
async def update(id: int, request: schemas.CreateUpdate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first():
        if query.first().owner_id == user_id.id:
            query.update(request.model_dump(), synchronize_session = False)
            db.commit()
        else:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You are not authorized to delete this post!")
        return query.first()
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "The ID you are searching is not found!")
 