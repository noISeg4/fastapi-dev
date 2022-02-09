# Base needed to create models
from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, Column, String, text, ForeignKey
from sqlalchemy.orm import relationship

#--------------------------------Model for posts table --------------------------------
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key= True, nullable= False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, nullable = False, server_default= 'true')
    created_at = Column(TIMESTAMP(timezone= True), nullable= False, server_default=text('now()'))
    
    # setting foreign key to users table with ondelete
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable= False)

    # relationship will get the related user from users table
    owner = relationship("User")

#-------------------------------- Model for users table --------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, nullable= False)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), nullable= False, server_default=text('now()'))

#--------------------------------Model for votes table --------------------------------
class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), primary_key= True, nullable= False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), primary_key= True, nullable= False)
