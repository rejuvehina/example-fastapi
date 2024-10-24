from fastapi import FastAPI, HTTPException, Response, status
import psycopg
from psycopg.rows import dict_row
from time import sleep
from pydantic import BaseModel


while True:
    try:
        conn = psycopg.connect(host="localhost", dbname="fastapi", user="postgres", password="Tangyujia2008444", row_factory=dict_row)
        cursor = conn.cursor()
        print("We have successfully connect to our database!")
        break
    except Exception as error:
        print("We have something wrong!!!!!")
        print(error)
        sleep(5)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


app = FastAPI()

@app.get("/posts")
async def get_request():
    cursor.execute("""SELECT * FROM posts""")
    all = cursor.fetchall()
    return {"data": all}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
async def new_post(para: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) Values (%s, %s, %s) RETURNING *""", (para.title, para.content, para.published))
    data = cursor.fetchone()
    conn.commit()
    return {"data": data}

@app.get("/posts/{id}")
async def get_individual(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    data = cursor.fetchone()
    if data:
        return {"data": data}
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "The ID you are searching is not found!")
    
@app.delete("/posts/{id}")
async def delete(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(id,))
    fetched = cursor.fetchone()
    conn.commit()
    if fetched:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "The ID you are searching is not found!")
    
@app.put("/posts/{id}")
async def update(id: int, request: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (request.title, request.content, id))
    fteched = cursor.fetchone()
    conn.commit()
    if fteched:
        return {"data": fteched}
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "The ID you are searching is not found!")

