from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel   # For pydantic schema
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor  # to get the column names

# Pydantic model for the post request
# Every field will matched for the data type
class PostModel(BaseModel):
    title: str                      # Required field
    content: str                    # Required field
    published: bool = False         # Optional field with default value
    #rating: Optional[int] = None    # Optional field with default as Null

app = FastAPI()

# Storing posts temporarily instead of DB
my_posts = [{"title":"title of post 1", "content":"content of post 1", "id": 1}, 
            {"title":"title of post 2", "content":"content of post 2", "id": 2},
            {"title":"title of post 3", "content":"content of post 3", "id": 3},
            {"title":"title of post 4", "content":"content of post 4", "id": 4},
            {"title":"title of post 5", "content":"content of post 5", "id": 5}]

def find_post(id):
    for post in my_posts:
        if(post["id"] == id):
            return post

def find_post_index(id):
    for idx, post in enumerate(my_posts):
        if(post["id"] == id):
            return idx


@app.get("/")
async def root():
    return {"message":"Welcome to my world reloaded"}



# ----------------------Get all posts-----------------------
@app.get("/posts")
def get_posts():
    return {"data": my_posts}                    # fastAPI will convert the list to JSON object and return to client



# ----------------------Create post-----------------------
@app.post("/posts", status_code= status.HTTP_201_CREATED)    # Default 200 OK is sent, but whenever something is created 201 should be sent
def create_posts(post: PostModel):
    post_dict = post.dict()                       # converting post model to dict -> adding ID -> adding to my_posts
    post_dict['id'] = len(my_posts) + 1
    #post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}



# ----------------------Get specific post----------------------
@app.get("/posts/{id}")                           # ID passed in request will be captured by id here
def get_post(id : int):                           # id received in str format, convert to int
    post = find_post(id)
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,         # post not found, revert with 404 Not Found error
                            detail= f"post with id {id} not found")         # with message
    
    return {"post_detail": post}



# ----------------------delete a post----------------------
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)          # Whenever something deleted, 204 is returned without any message so just sending Response
def delete_post(id: int):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} deos not exist")
    
    my_posts.pop(index)
    
    #return {"message": f"post {id} was successfully deleted"}
    return Response(status_code= status.HTTP_204_NO_CONTENT)



# ----------------------update a post----------------------
@app.put("/posts/{id}")
def update_post(id: int, post: PostModel):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} deos not exist")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    
    return {"data": post_dict}
