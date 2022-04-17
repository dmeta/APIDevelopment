from fastapi.testclient import TestClient
from fastapi import FastAPI
import os, sys;
from app.main import app
#from app import Schemas, models
import pytest
from alembic import command



from app.config import settings
from sqlalchemy import create_engine
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
    print ("Damian 50")

    #print ("******************* My session fixture ran: function *******************")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    print ("Damian 60")

@pytest.fixture(scope=scope)
def client(session):

    print ("Damian 30")

    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    #run our code before we run our test

    print ("Damian 40")
    #Using Alembic
    #command.downgrade("base")
    #command.upgrade("head")

    app.dependency_overrides[get_db] = override_get_db
    print ("Damian 50")
    yield TestClient(app)
    print ("Damian 60")

    #run our code after we run our test
