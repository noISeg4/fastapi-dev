# Pydantic models for Request/Response 

from datetime import datetime
from email.errors import NonPrintableDefect
from os import access
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

#-------------------User Model---------------------------
class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

# password NOT sent in reponse
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


#-------------------Post Model---------------------------
class PostBase(BaseModel):
    title: str                    
    content: str
    published: bool = True

# Inherting from PostBase
class PostCreate(PostBase):
    pass

# Inherting from PostBase
class PostUpdate(PostBase):
    pass

# Restricting the data sent in response, All the fields mentioned only will be sent in response

# Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, 
# but an ORM model (or any other arbitrary object with attributes).
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int                            # for newly added column represents user_id
    owner: UserResponse                      # user details to which the post belongs

    class Config:
        orm_mode = True


# {
#     "Post": {
#         "title": "first post",
#         "published": true,
#         "owner_id": 22,
#         "id": 1,
#         "content": "some random data",
#         "created_at": "2022-02-02T23:18:43.382005+05:30"
#     },
#     "votes": 2
# }

class PostResponseWithVotes(BaseModel):
    Post: PostResponse
    votes: int

#-------------------User login Model---------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ------------------Token Schema-------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

#-------------------- Vote Schema -----------------------
class VoteBase(BaseModel):
    post_id: int
    direction: conint(le=1)   # restrict to 0,1 but we can have negative values here coz of conint