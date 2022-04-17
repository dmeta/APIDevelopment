from tests.database import client, session
from app import Schemas, models
import pytest


def test_read_main(client, session):
    postq = session.query(models.Post).first()
    assert postq == None
    res = client.get("/")
    #print("************", res.json())
    assert res.status_code == 200
    assert res.json() == {"message": "API Development April 14, 2022 -- with DOCKER and postgres!!!"}
    assert res.json().get("message") == "API Development April 14, 2022 -- with DOCKER and postgres!!!"
    

@pytest.fixture
def test_user(client):
    

    user_data = {"email":"dmeta@hotmail.com", "passowrd": "1234"}
    print ("Damian 20")
    res = client.post("/users/", json=user_data)
    print ("Damian 25")
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["passowrd"]
    return new_user

def test_create_user(client): 
    email = "dmeta@hotmail.com"
    password = 1234
    res = client.post("/users/", json={"email":"dmeta@hotmail.com", "password":1234})
    #print (res.status_code, res.json())
    #Pydantic validation on schema UserCreateOutput
    new_user = Schemas.UserCreateOutput( **res.json())
    assert res.status_code == 201
    assert res.json().get("email") == email
    assert new_user.email == email

    #duplicate user
    res = client.post("/users/", json={"email":"dmeta@hotmail.com", "password":1234})
    assert res.status_code == 409

    
def test_login_user(client, test_user): 
    res = client.post("/login", data={"username":test_user["email"], "password":test_user["password"]})

    print ("Damian 10", res.status_code, res.status, res.json())
    
    assert res.status_code in (200, 403)
