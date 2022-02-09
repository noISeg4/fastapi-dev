from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel              # For pydantic schema
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor  # to get the column names

from . import schemas                       # to import pydantic models

from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

# For creating all the database tables based on the models when the app starts up
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#-------------------Testing SQLALCHEMY------------------
@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):      # To get the session
    posts = db.query(models.Post).all()
    #print(db.query(models.Post))                  # prints the QUERY
    return {"data":posts}


@app.get("/")
async def root():
    return {"message":"Welcome to my world reloaded"}



# ----------------------Get all posts-----------------------
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts """)
    
    posts = db.query(models.Post).all()
    #print(db.query(models.Post))                  # prints the QUERY
    return {"data": posts}



# ----------------------Create post-----------------------
@app.post("/posts", status_code= status.HTTP_201_CREATED)    # Default 200 OK is sent, but whenever something is created 201 should be sent
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #               (post.title, post.content, post.published))

    # new_post = models.Post(
    #     title= post.title,
    #     content = post.content,
    #     published = post.published
    # )

    # Shorter way of filling all the fields manually
    new_post = models.Post( **post.dict())
        
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}



# ----------------------Get specific post----------------------
@app.get("/posts/{id}")                           
def get_post(id : int,  db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))

    post = db.query(models.Post).filter(models.Post.id == id).first()       # .first() so as to fetch the first result otherwise 
                                                                            #  recursive search
    #print(post)
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,         # post not found, revert with 404 Not Found error
                            detail= f"post with id {id} not found")         # with message
    
    return {"post_detail": post}



# ----------------------delete a post----------------------
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)          # Whenever something deleted, 204 is returned without any message so just sending Response
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
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #               (post.title, post.content, post.published, str(id)))

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} deos not exist")
    
    post_query.update(post.dict(), synchronize_session= False)
    db.commit()

    return {"data": post_query.first()}
