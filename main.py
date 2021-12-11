import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND   

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

while 1:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='112121', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("*********************************")
        print("Database Connection Is Succesfull")
        print("*********************************")
        break

    except Exception as error:
        print('connection is failed')
        print('Error: ', error)
        time.sleep(5)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},{"title": "my favorite meals", "content": "I like icecream", "id": 2}, {"title": "Do you like my photos?", "content": "yes very nice", "id": 3}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "HELLO WORLD! I'm still here and in windows"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    #print(posts)
    return{"data": posts}

@app.post("/posts", status_code=HTTP_201_CREATED)  
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published)  VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data": new_post}
    #return{"new_message": f"title: {PayLoad['title']} content:{PayLoad['content']}"}   
    
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"error message": f"post with id: {id} doesn't exist"}
    print(post)
    return{"post_details": post}

@app.delete("/posts/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")

    #return{"message": f"post {id} was deleted"}
    return Response(status_code=HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")

    return{"data": updated_post}
