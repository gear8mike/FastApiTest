from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND   

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
    return {"message": "HELLO WORLD! I'm still here"}

@app.get("/all_posts")
def get_posts():
    return{"data": my_posts}

@app.post("/posts", status_code=HTTP_201_CREATED)  
def create_posts(post: Post):
    #print(post.rating)
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return{"data": post_dict}
    #return{"new_message": f"title: {PayLoad['title']} content:{PayLoad['content']}"}   
    
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"error message": f"post with id: {id} doesn't exist"}
    print(post)
    return{"post_details": post}

@app.delete("/posts/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # logic for deleting post
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")

    my_posts.pop(index)
    #return{"message": f"post {id} was deleted"}
    return Response(status_code=HTTP_204_NO_CONTENT)
