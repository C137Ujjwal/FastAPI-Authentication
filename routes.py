from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import models
import schemas
from fastapi import APIRouter
from config import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.CreatePost])
def test_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post


@router.get("/{id}", response_model=List[schemas.CreatePost])
def test_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{id} is not in the db"
        )
    return post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[schemas.CreatePost]
)
def test_create_post(post_post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return [new_post]
    # sync session
    # return with a status code 200


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def test_delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if not deleted_post.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{id} is not in the db"
        )
    deleted_post.delete(synchronize_session=False)
    db.commit()


@router.put('/posts/{id}', response_model=schemas.CreatePost)
def update_test_post(update_post:schemas.PostBase, id:int, db:Session = Depends(get_db)):

    updated_post =  db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
    updated_post.update(update_post.dict(), synchronize_session=False)
    db.commit()


    return  updated_post.first()