from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Annotated, Optional

# from pydantic.types import conint

"""
extends the BaseModel from pydantic lib to validate certain variables.

Use this approach to validate any given params.
for POST request, it's strongly recommended to use thus pydantic validation
This ensure that when a user wants to create a post, the request
will only go through if it has everything this class defines
"""
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # default value to TRUE, this becomes optional with value
    # rating: Optional[int] = None # fully optional field

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    # owner: UserOut # return the pydantic model from a different class

    """
    We use this config inner class to override the default return type object
    to be a standard python dictionary. Not configuring this class will yield and
    error in the class whose return data is dependent on this scheme.
    """
    class config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

class UserCreate(BaseModel):
    email: EmailStr # validate email using pydantic lib
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)] # conint = count integer that provides validation boundary



