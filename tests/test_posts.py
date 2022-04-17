from typing import List
from app import Schemas
import pytest


def test_authorized_user_get_all_posts(authorized_client, test_post):
    #print( "Damian test_authorized_user_get_all_posts 10: ", authorized_client, "*****", test_user)

    res = authorized_client.get("/posts/")
    posts = res.json()
    assert len(posts) == len(test_post)
    #print( "Damian test_authorized_user_get_all_posts 20: ", res.json())
    assert res.status_code == 200

    def validate(post):
        return Schemas.PostOut(**post)

    post_map = list(map(validate, res.json()))
    #print( "Damian test_authorized_user_get_all_posts 30: ", post_map)
    
def test_unauthorized_user_get_all_posts(client, test_post):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_post):
    res = authorized_client.get(f"/posts/8888888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 200

    #Validate Pydantic schema
    #print( "Damian test_get_one_post 10: ", res.json(), "***************", test_post[0].content)
    post = Schemas.UpdatePost(**res.json())
    #print( "Damian test_get_one_post 20: ", post)
    assert post.id == test_post[0].id
    #print( "Damian test_get_one_post 30: ", post.Post.content)
    assert post.content == test_post[0].content
    assert post.title == test_post[0].title
    assert post.published == test_post[0].published
    

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title 1", "awesome new content 1", True),
    ("awesome new title 2", "awesome new content 2", False),
    ("awesome new title 3", "awesome new content 3", True)])
def test_create_post(authorized_client, test_user, test_post, title, content, published):
    #print ("Damian  test_create_post 10: ", title, content, published)
    res = authorized_client.post("/posts/", json={"title":title, "content":content, "published":published})
    #print ("Damian  test_create_post 20: ", res, res.json())
    created_post = Schemas.UpdatePost(**res.json())
    #print ("Damian  test_create_post 30: ", created_post)
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"] 


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title 1", "awesome new content 1", None),
    ("awesome new title 2", "awesome new content 2", None),
    ("awesome new title 3", "awesome new content 3", None)])
def test_create_post_default_publised_True (authorized_client, test_user, test_post, title, content, published):
    #print ("Damian  test_create_post_default_publised 10: ", title, content, published)
    res = authorized_client.post("/posts/", json={"title":title, "content":content, "published":published})
    #print ("Damian  test_create_post_default_publised 20: ", res, res.json())
    created_post = Schemas.UpdatePost(**res.json())
    #print ("Damian  test_create_post_default_publised 30: ", created_post)
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"] 


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title 1", "awesome new content 1", None),
    ("awesome new title 2", "awesome new content 2", True),
    ("awesome new title 3", "awesome new content 3", False)])
def test_unauthorized_user_create_post(client, test_user, test_post, title, content, published):
    res = client.post("/posts/", json={"title":title, "content":content, "published":published})
    #print ("Damian  test_unauthorized_user_create_post 10: ", res, res.json())
    assert res.status_code == 401

def test_unautherized_user_delete_post(client, test_user, test_post):
    res = client.delete(f"/posts/{test_post[0].id}")
    #print ("Damian test_unautherized_user_delete_post 20: ", res, res.json())
    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"
    
def test_autherized_user_delete_post_success(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")
    #print ("Damian test_autherized_user_delete_post_success 20: ", res.status_code)
    assert res.status_code == 204
    #assert res.json().get("detail") == "Not authenticated"

def test_autherized_user_delete_post_not_exists(authorized_client, test_user, test_post):
    # post number 4 was created from test_user2 and test_user... It has to reject with code 
    res = authorized_client.delete(f"/posts/{test_post[3].id}")

    #print ("Damian test_autherized_user_delete_post_not_exists 20: ", res.status_code)
    assert res.status_code == 404
    #assert res.json().get("detail") == "Not authenticated"


def test_update_post (authorized_client, test_user, test_post):
    data = {
        "title":"updated title", 
        "content":"updated content",
        "id":test_post[0].id
    }
    res = authorized_client.put(f"/posts/{test_post[0].id}", json=data)
    #print ("Damian test_update_post 20: ", res.status_code, res.json())

    updated_post = Schemas.UpdatePost(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]



def test_update_other_post (authorized_client, test_user,test_user2, test_post):
    data = {
        "title":"updated title", 
        "content":"updated content",
        "id":test_post[3].id
    }
    res = authorized_client.put(f"/posts/{test_post[3].id}", json=data)
    #print ("Damian test_update_post 20: ", res.status_code, res.json())

    #updated_post = Schemas.UpdatePost(**res.json())
    assert res.status_code == 404
    #assert updated_post.title == data["title"]
    #assert updated_post.content == data["content"]


def test_unautherized_user_update_post(client, test_user, test_post):
    res = client.put(f"/posts/{test_post[0].id}")
    #print ("Damian test_unautherized_user_update_post 20: ", res.status_code, res.json())
    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"


def test_autherized_user_update_post_not_exists(authorized_client, test_user, test_post):
    # post number 4 was created from test_user2 and test_user... It has to reject with code 
    data = {
        "title":"updated title", 
        "content":"updated content",
        "id":test_post[3].id
    }
    res = authorized_client.put(f"/posts/8888888", json=data)

    #print ("Damian test_autherized_user_update_post_not_exists 20: ", res.status_code)
    assert res.status_code == 404
    #assert res.json().get("detail") == "Not authenticated"

