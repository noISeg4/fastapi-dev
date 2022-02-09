from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel              # For pydantic schema
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor  # to get the column names

from . import schemas                      # to import pydantic models
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

from . import utils


# For creating all the database tables based on the models when the app starts up
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message":"Welcome to my world reloaded"}


# ----------------------Get all posts-----------------------
# ERROR:: Query responds with list of posts and pydantic model trying to convert into single PostResponse
# Hence reponse_model will be the list of PostResponse

@app.get("/posts", response_model= List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts """)
    
    posts = db.query(models.Post).all()
    #print(db.query(models.Post))
    return posts



# ----------------------Create post-----------------------
@app.post("/posts", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #               (post.title, post.content, post.published))

    # Shorter way of filling all the fields manually
    new_post = models.Post( **post.dict())
        
    db.add(new_post)
    db.commit()

    # Query returns sqlalchemy model and is processed by pydantic model, 
    # For this transition to work add orm_mode = True in pydnatic schema
    db.refresh(new_post)
    return new_post



# ----------------------Get specific post----------------------
@app.get("/posts/{id}", response_model= schemas.PostResponse)                           
def get_post(id : int,  db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))

    post = db.query(models.Post).filter(models.Post.id == id).first()       # .first() so as to fetch the first result otherwise 
                                                                            #  recursive search
    #print(post)
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,         # post not found, revert with 404 Not Found error
                            detail= f"post with id {id} not found")         # with message
    
    return post



# ----------------------delete a post----------------------
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} does not exist")
    
    post_query.delete(synchronize_session= False)
    db.commit()

    #return {"message": post_query}
    return Response(status_code= status.HTTP_204_NO_CONTENT)



# ----------------------update a post----------------------
@app.put("/posts/{id}", response_model= schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #               (post.title, post.content, post.published, str(id)))

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} deos not exist")
    
    post_query.update(post.dict(), synchronize_session= False)
    db.commit()

    return post_query.first()


#-----------------------------Create User--------------------------------
@app.post("/users", status_code= status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_users(User: schemas.UserCreate, db: Session = Depends(get_db)):

    User.password = utils.hash(User.password)
    new_user = models.User( **User.dict())
        
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

#-----------------------------retrieve specific User--------------------------------
@app.get("/users/{id}", response_model= schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"user with id {id} not found")
    
    return user
