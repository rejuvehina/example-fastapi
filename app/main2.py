import secrets
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# this is the command told sqlalchemy to run the create statement so it can generate all the tables when it starts up
# unimodels.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "hello world!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


    