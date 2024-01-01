from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

"""
This will create all the tables configured in the Base class as soon
as the app is started

from models package -> Base (parent class of the Post class/Inheritance)
-> Metadata from the library -> create_all by binding the engine as the source DB
"""
# models.Base.metadata.create_all(bind=engine) --> Commented out as this app is using alembic as the DB source control

"""
Create an instance of FastAPI

To run the web server, use uvicorn lib with the following syntax
- uvicorn {your main}:{app instance} --reload
- --reload is a special lib to auto reload when code was modified
"""
app = FastAPI()

origins = ["*"] 

# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
        
# calling the router that we set inside "routers" folder
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Successfully deployed to Heroku using automated pipeline"}