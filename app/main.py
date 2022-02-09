from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote            # Route requests to other files
from .config import settings
from fastapi.middleware.cors import CORSMiddleware     # for CORS

# For creating all the database tables based on the models when the app starts up
# Commented bcoz now using alembic for creating and migrating Database
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins= ['*']                        # To allow all domains
# origins= ['https://www.google.com']  

app.add_middleware(
    CORSMiddleware,                   # All request first goes through CORSMiddleware
    allow_origins= origins,           # What domains are allowed
    allow_credentials= True,
    allow_methods= ["*"],             # allow specific HTTP methods
    allow_headers= ["*"],             # allow specific HTTP methods
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message":"Welcome to my world reloaded, IT WORKS DOPE"}