from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

"""
Defining oauth scheme for user login and access;
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
"""
Python JWTJSON Web Token is a succinct, URL-safe mechanism to represent claims that need to be exchanged between two parties (JWT). It is frequently used to transport data between computers and authenticate users securely.

JOSE is one of the most used libs in python to handle JWT token creation
"""
#SECRET_KEY
SECRET_KEY = settings.secret_key # string from rand hex 32 according to the documentation
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

"""
./auth/POST(login)
"""
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    """
    to_encode becomes
    {
        "user_id": {user_id}
        "exp": {time expiration}
    }
    """

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

"""
Any request made requires a token and therefore this method provides
a functionality to check whether the given token is valid or not
"""
def verify_access_token(token: str, credentials_exception):
    try:
        # decode the payload included in the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = str(payload.get("user_id")) # cast the original int user id to str

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

"""
Create a dependency class that is used on a specific router
"""    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
     
    return user