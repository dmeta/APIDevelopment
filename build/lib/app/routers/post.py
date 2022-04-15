from fastapi.security.oauth2 import OAuth2
from .. import models, Schemas, utils, oauth2
from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
from .. database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional


router = APIRouter(prefix = "/posts", tags = ["Posts"])

#@router.get("/", response_model=list[Schemas.UpdatePost])
#@router.get("/")
@router.get("/", response_model=list[Schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
                 current_user: str = Depends(oauth2.get_current_user),
                 limit: int = 10, skip: int = 0,
                 searchtitle: Optional[str] = "", 
                 id_filter: Optional[int] = -1):
    #print (db.query(models.Post))
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id)\
    #    .filter(models.Post.title.contains(searchtitle))\
    #    .order_by(models.Post.id)\
    #    .offset(skip)\
    #    .limit(limit).all()

    #####********** borrar filter
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)
    if str(searchtitle) != "":
        print ("searchtitle ************* ", searchtitle )
        results = results.filter(models.Post.title.contains(searchtitle))
    if id_filter != -1:
        results = results.filter(models.Post.id == id_filter)
    
    results = results\
        .order_by(models.Post.id)\
        .offset(skip)\
        .limit(limit)

    print (results)
    results = results.all()


    #print (results)
    return results


@router.get("/{id}", response_model=Schemas.UpdatePost)
def get_posts(id: int, db: Session = Depends(get_db), 
                 current_user: str = Depends(oauth2.get_current_user)):
    #print(db.query(models.Post).filter(models.Post.id== id))
    post = db.query(models.Post).filter(models.Post.id == id, models.Post.owner_id== current_user.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"message": f"postid {id} was not found"})
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schemas.UpdatePost)
def create_posts(post: Schemas.PostInput, db: Session = Depends(get_db), 
                 current_user: str = Depends(oauth2.get_current_user)):
    #print ("current_user: ", current_user.email)
    #1 option 1
    new_post = models.Post(title=post.title, content = post.content, published = post.published)

    #2 another way to identify all fields
    new_post = models.Post(owner_id = current_user.id,  **post.dict())


    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #print (post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                 current_user: str = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id , models.Post.owner_id == current_user.id)

    #print (post)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"message": f"postid {id} was not found"})
    else:
        post.delete (synchronize_session = False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Schemas.UpdatePost)
def put_post(id: int, upd_post: Schemas.PostInput, db: Session = Depends(get_db), 
                 current_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id , models.Post.owner_id == current_user.id)
    #print (post_query )
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    else:
        post_query.update(upd_post.dict())
        db.commit()
        return post_query.first()


