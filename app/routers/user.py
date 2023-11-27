from fastapi import status, HTTPException, Depends, APIRouter  
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
) # special method from fastAPI to generate a router to be called from the main app
"""-------------------- User Creation section --------------------"""

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> dict:
    # hash the password from user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    print(user)
    new_user = models.User(
       **user.model_dump() # ** as the operator to unpack the dictionary in ordered manner
    )
    db.add(new_user) # add to the db
    db.commit() # commit the changes
    db.refresh(new_user) # return the committed changes back to the Var

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND # status lib from fast api
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return user