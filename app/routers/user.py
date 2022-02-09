from fastapi import APIRouter, FastAPI, Response, status, HTTPException, Depends

from .. import schemas
from .. import models
from .. import utils

from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/users",
    tags = ["user"]
)

#-----------------------------Create User--------------------------------
# @router.post("/users", status_code= status.HTTP_201_CREATED, response_model= schemas.UserResponse)
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_users(User: schemas.UserCreate, db: Session = Depends(get_db)):

    User.password = utils.hash(User.password)
    new_user = models.User( **User.dict())
        
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

#-----------------------------retrieve specific User--------------------------------
# @router.get("/users/{id}", response_model= schemas.UserResponse)
@router.get("/{id}", response_model= schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"user with id {id} not found")
    
    return user