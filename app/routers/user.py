from starlette.status import HTTP_409_CONFLICT
from .. import models, Schemas, utils
from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
from .. database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix = "/users", tags = ['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schemas.UserCreateOutput)
def create_user(user: Schemas.UserCreate, db: Session = Depends(get_db)):
    # print ("Damian post 10: ", user)
    userdb = db.query(models.User).filter(models.User.email == user.email).first()
    # print ("Damian post 20: ", userdb)
    #print(user.email)
    if userdb:
        # print ("Damian post 25: ")
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail= f"Email {user.email} duplicated")

    #hash the Password
    hashpwd = utils.hash(user.password)
    # print ("Damian post 30 hashpwd: ", hashpwd)
    user.password = hashpwd 

    #another way to identify all fields
    # print ("Damian post 40: ", user)
    new_user = models.User(**user.dict())
    # print ("Damian post 50: ", user)

    try:
        db.add(new_user)
        db.commit()
        # # print ("Damian post 55: Commit")
    except exc.SQLAlchemyError:
        # # print ("Damian post  56: Error")
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail= exc.SQLAlchemyError)

    
    # print ("Damian post 60: ", user)
    # print ("Damian post 70: ", user)
    db.refresh(new_user)
    # print ("Damian post 80 new_user: ", new_user.email)
    #print (post)
    return new_user

@router.get("/{id}", status_code =status.HTTP_200_OK, response_model=Schemas.UserCreateOutput)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user


