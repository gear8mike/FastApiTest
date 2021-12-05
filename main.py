from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange   

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},{"title": "favorite meals", "content": "I like icecream", "id": 2}]

@app.get("/")
async def root():
    return {"message": "HELLO WORLD! I'm still here"}

@app.get("/posts")
def get_posts():
    return{"data": my_posts}

@app.post("/posts")  
def create_posts(post: Post):
    #print(post.rating)
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return{"data": post_dict}
    #return{"new_message": f"title: {PayLoad['title']} content:{PayLoad['content']}"}   
    