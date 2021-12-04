from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "HELLO WORLD! I'm still here"}

@app.get("/posts")
def get_posts():
    return{"data": "your posts"}

@app.post("/createposts")  
def create_posts(post: Post):
    print(post.rating)
    print(post.dict())
    return{"data": "new post"}
    #return{"new_message": f"title: {PayLoad['title']} content:{PayLoad['content']}"}   
    