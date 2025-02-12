import logging
from fastapi import status, HTTPException, Depends, APIRouter  
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    tags=['Authentication']
)

"""
OAuth2 Login Endpoint: Authenticates users and returns an access token.

OAuth2PasswordRequestForm sends form data:
{
    "username": "user@example.com",
    "password": "securepassword"
}
"""
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    """
    Authenticate user and return JWT token.

    Steps:
    1. Retrieve user from DB by email (username field).
    2. If the user doesn't exist, return a 403 error.
    3. Validate the password using the utils.verify function.
    4. If valid, generate and return an access token.
    """

    logger.info(f"Login attempt for user: {user_credentials.username}")

    # Step 1: Query user from the database based on email (username field)
    user = db.query(models.User).filter(
                    models.User.email == user_credentials.username
                    ).first()

    # Step 2: If user is not found, log and return an error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    
    # Step 3: Validate password using utils.verify
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    
    # Step 4: Generate JWT token with user ID as payload
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}