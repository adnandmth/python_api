from fastapi import Response, status, HTTPException, Depends, APIRouter  
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

"""
https://fastapi.tiangolo.com/reference/apirouter/
prefix -> An optional path prefix for the router.
"""
router = APIRouter(
    prefix="/posts",
    tags=['Posts'] # group router based on its functionality
)

"""
Test sqlalchemy db engine connection,

all of the configurations are coming from the
fast api library docs which almost all of them
are copy paste contents and we don't have know
anything behind them!

Depends -> it creates a dependency in the database we are going to use
and it calls get_db as the dependency where each request generates a new 
session that is derived from the Session method
"""
@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(
    db: Session = Depends(get_db), 
    current_user : int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "") -> dict:
    """
    commented query cursor is when using psycopg2 as the query tool
    """

    print(current_user)
    # cursor.execute(
    #     """
    #     SELECT * FROM posts
    #     """
    # )
    # posts = cursor.fetchall( )
    # print(posts)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(posts)

    """
    Perform a join using sqlaclhemy

    By default join clause syntax returns a INNER
    and we need to pass the 3rd argument to specify the OUTER LEFT clause
    """
    results = db.query(
        models.Post, func.count(models.Post.id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
                models.Post.id).filter(
                    models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    print(results)

    return results

"""
Body(...) is a special param provided by FastAPI
async def create_posts(payLoad: dict = Body(...)):

expected payload
- title : str
- content :  str

Args:
1. In the argument, we pass the Post class reference for which
the class itself inherits the BaseModel lib from FastAPI.
The post class then will validate the given params it has everything needed
2. Dependency using Depends lib that calls get_db anytime this route is called
3. Dependency using Depends lib that calls get_current_user anytime this route is called
    oauth.get_current_user --> verify_access_token
        user is enforced to send the granted token as the header of the request

Decorator:
2nd argument decorator is to set the default http status when the someone sends a new data
3rd argument decorator is to set the response default instead of hardcoded return statement
"""    
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user : int = Depends(oauth2.get_current_user)) -> dict:
    # print(post.rating)
    # post_dict = post.model_dump() # dict is deprecated and therefore use model_dump
    # post_dict['id'] = randrange(0, 100000)
    # my_posts.append(post_dict)
    # post_dict = post.model_dump()
    # print(post_dict)

    """
    commented query cursor is when using psycopg2 as the query tool
    """
    # cursor.execute(
    #     """
    #     INSERT INTO posts(title, content, published)
    #     VALUES(%s, %s, %s)
    #     RETURNING *
    #     """, 
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit() # commit the changes, no data will be stored in the DB if this is not executed

    print(f"--- current user --- : {current_user}")

    new_post = models.Post(
        owner_id=current_user.id, # Post requires user_id hence we take user id from the logged in user
       **post.model_dump() # ** as the operator to unpack the dictionary in ordered manner
    )
    db.add(new_post) # add to the db
    db.commit() # commit the changes
    db.refresh(new_post) # return the committed changes back to the Var
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(
    id: int, 
    db: Session = Depends(get_db), 
    current_user : int = Depends(oauth2.get_current_user)) -> dict:
    """
    commented query cursor is when using psycopg2 as the query tool
    """
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # post = find_post(id)

    post = db.query(
        models.Post, func.count(models.Post.id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
                models.Post.id).filter(models.Post.id == id).first()
    print(type(post))

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND # status lib from fast api
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db), 
    current_user : int = Depends(oauth2.get_current_user)):

    """
    commented query cursor is when using psycopg2 as the query tool
    """
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit() 

    # deleting post
    # find the index in the array that required id
    # index = find_index_post(id)

    post_todelete = db.query(models.Post).filter(models.Post.id == id)
    post_temp = post_todelete.first()

    if post_temp == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    if post_temp.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    post_todelete.delete(synchronize_session=False)
    db.commit

    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int, 
    updated_post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user : int = Depends(oauth2.get_current_user)) -> dict:
    """
    commented query cursor is when using psycopg2 as the query tool
    """
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, publish = %s WHERE id = %s RETURNING *""",
    #                 (post.title, post.content, post.publish, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit() 

    post_toupdate = db.query(models.Post).filter(models.Post.id == id)
    post_temp = post_toupdate.first()

    if post_temp == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    if post_temp.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    post_toupdate.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    # post_dict = post.model_dump() # dump the data from the frontend to a new dict
    # post_dict['id'] = id # append the id from the argument into the dict
    # my_posts[index] = post_dict # replace the existing post with the new dict
    return post_toupdate.first()