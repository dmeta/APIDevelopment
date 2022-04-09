from fastapi.testclient import TestClient
from app.main import app
from http import request


client = TestClient(app)

def test_root():
    res = client.get("/")
    message = res.json().get("message")
