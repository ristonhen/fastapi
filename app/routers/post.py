from fastapi import Response,status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List,Optional
from .. import models, schemas ,oauth2
from ..database import get_db



router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model=List[schemas.UserBase])
def get_post(db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user),
             limit: int = 100,skip: int = 0,search: Optional[str] = ""):
    # Get one post current owner user login
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.user_id).all()
    # Search post
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return  posts

############### create posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate ,db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id = current_user.user_id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.UserBase)
def get_post(id: str, db: Session = Depends(get_db)
             ,current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post whith id: {id} was not found")
    # For get post on current user_login
    # if post.owner_id != current_user.user_id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                         detail= "Not authorized to perform requested action")
    return post
    

# delete post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query  = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= "Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query  = db.query(models.Post).filter(models.Post.id == str(id))
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= "Not authorized to perform requested action")
    post_query.update(updated_post.dict(),synchronize_session=False)
    
    db.commit()
    return post_query.first()