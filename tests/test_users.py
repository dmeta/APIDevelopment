#from tests.database import client, session
from app import Schemas, models
import pytest
from jose import jwt
from app.config import settings

def test_read_main(client, session):
    postq = session.query(models.Post).first()
    assert postq == None
    res = client.get("/")
    #print("************", res.json())
    assert res.status_code == 200
    #assert res.json() == {"message": "API Development April 14, 2022 -- with DOCKER and postgres!!!"}
    #assert res.json().get("message") == "API Development April 14, 2022 -- with DOCKER and postgres!!!"
    


def test_create_user(client): 
    email = "dmeta@hotmail.com"
    password = "1234"
    res = client.post("/users/", json={"email":"dmeta@hotmail.com", "password":"1234"})
    #print (res.status_code, res.json())
    #Pydantic validation on schema UserCreateOutput
    new_user = Schemas.UserCreateOutput( **res.json())
    assert res.status_code == 201
    assert res.json().get("email") == email
    assert new_user.email == email

    #duplicate user
    res = client.post("/users/", json={"email":"dmeta@hotmail.com", "password":"1234"})
    assert res.status_code == 409

    
def test_login_user(client, test_user): 
    # print ("Damian test_login_client 10: ", test_user)
    res = client.post("/login", data={"username":test_user["email"], "password":test_user["password"]})
    login_res = Schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    id: str = payload.get("user_id")
    print ("Damian test_login_client 15: ", id, test_user)
    assert id == test_user["id"]

    # print ("Damian test_login_client 20: ", test_user)
    
    assert res.status_code in (200, 403)

@pytest.mark.parametrize("email, password, expected", [
    #("dmeta@hotmail.com", "1234", 200),
    ("dmeta@hotmail.com", "WrongPassword", 403),
    ("WrongUser", "1234", 403),
    (None, "1234", 422),
    ("WrongUser", None, 422 )])
def test_incorrent_login(test_user, client, email, password, expected):
    res = client.post("/login", data = {"username":email, "password":password})
    print ("Damian test_incorrent_login 10: ", res.json())
    assert res.status_code == expected
    #assert res.json().get("detail") == "Invalid credentials"
