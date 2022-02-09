from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
# For pydantic schema
from pydantic import BaseModel

# Pydantic model for the post request
# Every field will matched for the data type
class PostModel(BaseModel):
    title: str                      # Required field
    content: str                    # Required field
    published: bool = False         # Optional field with default value
    rating: Optional[int] = None    # Optional field with default as Null

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Welcome to my world reloaded"}

@app.get("/posts")
def get_posts():
    return {"data":"This is your post"}

@app.post("/createposts")

# Extract all fields in body from the request -> convert to dict -> save in payload
# payload: dict = Body(...)
# def create_posts(payload: dict = Body(...)):
    # print(payload)
    # return {"message":"Successfully created post"}
    # return {"new_post":f"Title: {payload['title']} Content: {payload['content']}"}

# Here payload will be saved in the pydantic model for post request 
# and will be validated against the datatype mentioned in model
def create_posts(post: PostModel):
    print(post)                                  # pydantic model => use . to access the keys
    print(post.title + " " + post.content)    
    print(post.dict())                           # convert pydantic model to dict
    return {"new_post": post}