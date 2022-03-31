from starlette.status import HTTP_409_CONFLICT
from .. import models, Schemas, utils
from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
from .. database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix = "/users", tags = ['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schemas.UserCreateOutput)
def create_user(user: Schemas.UserCreate, db: Session = Depends(get_db)):
    print(user)
    userdb = db.query(models.User).filter(models.User.email == user.email).first()
    #print(user.email)
    if userdb:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail= f"Email {user.email} duplicated")

    #hash the Password
    hashpwd = utils.hash(user.password)
    user.password = hashpwd 

    #another way to identify all fields
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    #print (post)
    return new_user

@router.get("/{id}", status_code =status.HTTP_200_OK, response_model=Schemas.UserCreateOutput)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user


