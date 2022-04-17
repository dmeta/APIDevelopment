#pytest -n 2 -v -s  --disable-warnings  tests/test_votes.py
import pytest


def test_vote_on_post(authorized_client, test_post):
    data = {"post_id": test_post[3].id, "dir":1}
    res = authorized_client.post("/vote/", json=data)
    print ("Damian test_vote_on_post 20: ", res.status_code, res.json())
    assert res.status_code == 201




def test_vote_twice_post(authorized_client, test_post):
    data = {"post_id": test_post[3].id, "dir":1}
    res = authorized_client.post("/vote/", json=data)
    #print ("Damian test_vote_on_post 20: ", res.status_code, res.json())
    assert res.status_code == 201

    # duplicated vote
    res = authorized_client.post("/vote/", json=data)
    #print ("Damian test_vote_on_post 30: ", res.status_code, res.json())
    assert res.status_code == 409
    assert res.json().get("detail") == "User 1 has already voted on that post 4"


def test_delete_vote(authorized_client, test_post):
    #create first vote
    test_id = test_post[3].id
    data = {"post_id":test_id, "dir":1}
    #print ("Damian test_delete_vote 10: ", data)
    res = authorized_client.post("/vote/", json=data)
    #print ("Damian test_delete_vote 20: ", res.status_code, res.json(), "**** Test_post:", t)
    assert res.status_code == 201

    data = {"post_id":test_id, "dir":0}
    #print ("Damian test_delete_vote 20: ", data)
    res = authorized_client.post("/vote/", json=data)
    assert res.status_code == 202

def test_delete_vote_not_exists(authorized_client, test_post):
    #create first vote
    test_id = test_post[3].id
    data = {"post_id":test_id, "dir":0}
    #print ("Damian test_delete_vote 10: ", data)
    res = authorized_client.post("/vote/", json=data)
    #print ("Damian test_delete_vote 20: ", res.status_code, res.json(), "**** Test_post:", test_id)
    assert res.status_code == 404


