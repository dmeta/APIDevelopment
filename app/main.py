#to execute in dev: uvicorn app.main:app --reload
#to execute on ubuntu: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
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
from fastapi.middleware.cors import CORSMiddleware

#import os
#import urllib.parse as up
#from typing import Optional
#from fastapi.exceptions import HTTPException
#from random import randrange
import sqlalchemy
from sqlalchemy.orm import Session
#from . import crud, models, schemas


#damian la creacion de la base si no existe no es mas necesario porque estamos usando alembic
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com", "https://youtube.com"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "API Development April 18, 2022 -- with DOCKER and postgres!!!"}
    