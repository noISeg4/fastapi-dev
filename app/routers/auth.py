from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas
from .. import models
from .. import utils
from .. import oauth2
from .. import database
from sqlalchemy.orm import Session
from typing import List

from fastapi.security.oauth2 import OAuth2PasswordRequestForm  # fetch the username and password from form-data in body

router = APIRouter(
    tags = ["Authentication"]
)

@router.post("/login", response_model= schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # We were sending email and password raw in body
    # OAuth2PasswordRequestForm requires the username and password are sent in form-data in body
    # In our case, email is stored in username and password in password
    # {"username": "sguleria@gmail.com", "password":"password"}

    # user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials")
    
    # verifying the password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials")
    
    # create token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    
    # can check the token data in https://jwt.io/
    return {"access_token": access_token, "token_type": "bearer"}

