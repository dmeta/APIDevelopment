from fastapi.testclient import TestClient
from fastapi import FastAPI
import os, sys;
from app.main import app
#from app import Schemas, models
import pytest
from alembic import command
from app.oauth2 import create_access_token
from app import models
from alembic import command

from app.config import settings
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
#create tables in fastapi_test table

engine = create_engine( SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#we dont need this line
#Base = declarative_base()

scope = "function" #possible values: function, module, session
@pytest.fixture(scope=scope)
def session():
    # print ("Damian session 10")
    Base.metadata.drop_all(bind=engine)
    # print ("Damian session 20")
    Base.metadata.create_all(bind=engine)
    # print ("Damian session 30")
    db = TestingSessionLocal()
    # print ("Damian session 40")
    try:
        # print ("Damian session 50")
        yield db
    finally:
        # print ("Damian session 60")
        db.close()
    # print ("Damian session 70")

@pytest.fixture(scope=scope)
def client(session):

    # print ("Damian Client 10")

    def override_get_db():
        # print ("Damian Client 20")
        try:
            # print ("Damian Client 22")
            yield session
            # print ("Damian Client 23")
        finally:
            # print ("Damian Client 24")
            session.close()
            # print ("Damian Client 25")
        # print ("Damian Client 30")
    #run our code before we run our test

    # print ("Damian Client 40")
    #Using Alembic
    #command.downgrade("base")
    #command.upgrade("head")

    app.dependency_overrides[get_db] = override_get_db
    # print ("Damian Client 50")
    client = TestClient(app)
    # print ("Damian Client 55", client)
    yield client
    # print ("Damian Client 60")

    #run our code after we run our test

@pytest.fixture(scope=scope)
def test_user(client):
    user_data = {"email":"dmeta@hotmail.com", "password": "1234"}
    # print ("Damian Test_user 20")
    res = client.post("/users/", json=user_data)
    # print ("Damian Test_user 25", res.status_code, res.json())
    assert res.status_code == 201
    # print ("Damian Test_user 30")
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture(scope=scope)
def test_user2(client):
    user_data = {"email":"dmeta1@hotmail.com", "password": "1234"}
    # print ("Damian Test_user 20")
    res = client.post("/users/", json=user_data)
    # print ("Damian Test_user 25", res.status_code, res.json())
    assert res.status_code == 201
    # print ("Damian Test_user 30")
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture(scope=scope)
def token(test_user):
    return create_access_token(data= {"user_id":test_user["id"]})

@pytest.fixture(scope=scope)
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture(scope=scope)
def test_post(test_user, session, test_user2):
    posts_data = [
        {"title":"first title","content":"first content","owner_id": test_user["id"]},
        {"title":"second title","content":"second content","owner_id": test_user["id"]},
        {"title":"third title","content":"third content","owner_id": test_user["id"]},
        {"title":"fourth title","content":"fourth content","owner_id": test_user2["id"]}]

    def create_post_model(post):
        #print("Damian create_post_model 10: ", post)
        res_post = models.Post(**post) 
        #print("Damian create_post_model 20: ", post)
        return res_post

    post_map = list(map(create_post_model, posts_data))
    #print("Damian test_post 20: ", post_map)

    session.add_all(post_map)
    session.commit()

    posts = session.query(models.Post).all()
    #print("Damian 40 test_post: ", posts[0] )
    return posts
