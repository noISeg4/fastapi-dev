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
    #rating: Optional[int] = None   # Optional field with default as Null

#------------------------------ Setting up connection to DB------------------------------
try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                            password='fastapidev', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connection to DB successful")
except Exception as error:
    print("Connection to DB failed")
    print("Error: ",error)

app = FastAPI()


@app.get("/")
async def root():
    return {"message":"Welcome to my world reloaded"}



# ----------------------Get all posts-----------------------
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    #print(posts)
    return {"data": posts}                    # fastAPI will convert the list to JSON object and return to client



# ----------------------Create post-----------------------
@app.post("/posts", status_code= status.HTTP_201_CREATED)    # Default 200 OK is sent, but whenever something is created 201 should be sent
def create_posts(post: PostModel):
    # Staging changes
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                  (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    
    # Make the changes to the database persistent
    conn.commit()
    return {"data": new_post}



# ----------------------Get specific post----------------------
@app.get("/posts/{id}")                           
def get_post(id : int):
    # convert the integer id to string id while sending to DB
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    #print(post)

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,         # post not found, revert with 404 Not Found error
                            detail= f"post with id {id} not found")         # with message
    
    return {"post_detail": post}



# ----------------------delete a post----------------------
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)          # Whenever something deleted, 204 is returned without any message so just sending Response
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    print(deleted_post)

    if not deleted_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} does not exist")
    
    #return {"message": deleted_post}
    return Response(status_code= status.HTTP_204_NO_CONTENT)



# ----------------------update a post----------------------
@app.put("/posts/{id}")
def update_post(id: int, post: PostModel):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
                  (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    #print(updated_post)

    if updated_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} deos not exist")

    return {"data": updated_post}
