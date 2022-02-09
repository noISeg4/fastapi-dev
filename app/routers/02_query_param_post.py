from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas
from .. import models
from .. import utils

from ..database import get_db
from sqlalchemy.orm import Session

from typing import List, Optional

from .. import oauth2

router = APIRouter(
    prefix = "/posts",     # Remove repeating part in all path operation
    tags = ["posts"]       # group APIs based on tag
)

# ----------------------Get all posts-----------------------
@router.get("/", response_model= List[schemas.PostResponse])
# limit QUERY PARAM for limiting the number of posts returned
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute(""" SELECT * FROM posts """)
    
    print(limit)
    #posts = db.query(models.Post).all()

    # run the query with limit received in query params
    #posts = db.query(models.Post).limit(limit).all()
    
    # run the query limit and skip -> skil number of times
    #posts = db.query(models.Post).limit(limit).offset(skip).all()

    # filtering based on search key on title
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts



# ----------------------Create post-----------------------)
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
# user_id: int = Depends(oauth2.get_current_user) forces the user to be logged in 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    print(current_user.password)

    new_post = models.Post(owner_id = current_user.id, **post.dict())       # owner_id fetched from token
    db.add(new_post)
    db.commit()

    db.refresh(new_post)
    return new_post



# ----------------------Get specific post----------------------
#@router.get("/posts/{id}", response_model= schemas.PostResponse)
@router.get("/{id}", response_model= schemas.PostResponse)                           
def get_post(id : int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))

    post = db.query(models.Post).filter(models.Post.id == id).first()       # .first() so as to fetch the first result otherwise 
                                                                            #  recursive search
    #print(post)
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,         # post not found, revert with 404 Not Found error
                            detail= f"post with id {id} not found")         # with message

    # Ensuring the post belongs to the user trying to delete post
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
    #                         detail= f"Not authorized to perform the action")

    return post



# ----------------------delete a post----------------------
#@router.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} does not exist")

    # Ensuring the post belongs to the user trying to delete post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= f"Not authorized to perform the action")
    
    post_query.delete(synchronize_session= False)
    db.commit()

    #return {"message": post_query}
    return Response(status_code= status.HTTP_204_NO_CONTENT)



# ----------------------update a post----------------------
#@router.put("/posts/{id}", response_model= schemas.PostResponse)
@router.put("/{id}", response_model= schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #               (post.title, post.content, post.published, str(id)))

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} deos not exist")
    
    # Ensuring the post belongs to the user trying to delete post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= f"Not authorized to perform the action")
    
    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()

    return post

