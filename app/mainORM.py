#para executar o webserver: uvicorn app.mainORM:app --reload
from typing import Optional, List
from types import new_class
from fastapi import FastAPI#, Response, status, Depends, HTTPException
from fastapi.params import Body
from passlib.exc import PasswordSizeError
from pydantic import BaseModel
#import psycopg2
#from psycopg2.extras import RealDictConnection, RealDictCursor
#import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.visitors import CloningExternalTraversal
from starlette.status import HTTP_404_NOT_FOUND
#from app import models
from . import models, Schemas, utils
from . database import engine, get_db
from .routers import post, user, auth, vote

#import os
#import urllib.parse as up
#from typing import Optional
#from fastapi.exceptions import HTTPException
#from random import randrange
import sqlalchemy
from sqlalchemy.orm import Session
#from . import crud, models, schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return "API Development"



