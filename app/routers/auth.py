from fastapi import status, HTTPException, Depends, APIRouter  
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

"""
https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#oauth2passwordrequestform
"""
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    OAuth2PasswordRequestForm return a structured dictionary:
    {
        "username": "aaa",
        "password": "cccc"
    }
    """

    # query the user from DB based on the given username and password
    user = db.query(models.User).filter(
                    models.User.email == user_credentials.username
                    ).first()

    # if user not found then throw exception
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    
    # if password was not valid for the given username then throw exception
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    
    # if password is valid then create access token with user.id as the payload value
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}