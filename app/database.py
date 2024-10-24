from typing import Iterable
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep
from.config import settings

#"Type://<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# engine is responsible for conenction to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# In order to talk to a database, we need a session: 
# So every time we have a request, we are going to get a session; then the session is able to send SQL commands to database, then when the request is done, close it out.

SessionLocal = sessionmaker(bind=engine, autoflush= False)

# define our base class

Base = declarative_base()

# dependency: So every time we have a request, we are going to get a session; then the session is able to send SQL commands to database, 
# then when the request is done, close it out. So the get_db is kind of helpful every time we get a request to any of our API endpoints.

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", dbname="fastapi", user="postgres", password="Tangyujia2008444", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("We have successfully connect to our database!")
#         break
#     except Exception as error:
#         print("We have something wrong!!!!!")
#         print(error)
#         sleep(5)