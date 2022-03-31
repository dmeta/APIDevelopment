#para executar o webserver: uvicorn app.main:app --reload

from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.exceptions import HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()
my_posts=[{"title":"Beaches in Florida", "content":"Awesome beaches from Florida", "id":1}, {"title":"the grand cook book", "content":"best receipts", "id":2}]
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts_v1")
async def get_posts():
    return {"data": "this is your post"}

@app.post("/createposts")
async def create_posts(payLoad: dict = Body(...)):
    print (payLoad)
    return {"new post: ":f"title: {payLoad['title']}, content: {payLoad['content']}"}


@app.post("/createposts_validated")
async def create_postss(post: Post):
    print (post)
    print(post.dict())
    #return {"new post: ":f"title: {new_post['title']}, content: {new_post['content']}"}
    print ({"new post: ":f"title: {post.title}, content: {post.content}"})
    return {"data": post.dict()}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_postss(post: Post):
    print (post)
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000000)
    #return {"new post: ":f"title: {new_post['title']}, content: {new_post['content']}"}
    my_posts.append(post_dict)


    return {"data": my_posts}

def find_post(id):
    my_post = [x for x in my_posts if x['id'] == id]
    if my_post:
        my_post = my_post[0]
    print( my_post )
    return my_post 

def find_index_post(id: int):
    for i,p in enumerate(my_posts):
        print ("p", p )
        if p['id'] == id:
            print ("found")
            return i
    print ("not found")
    return None


@app.get("/posts/{id}", status_code=status.HTTP_201_CREATED)
def get_post(id: int, response: Response):
    print (id)
    post = find_post( id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"message": f"postid {id} was not found"})
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"postid {id} was not found"}
    return {"post detail": f"post {post}"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    ind = find_index_post(id)
    #print(id, ind , my_posts)
    if ind is not None:
        my_posts.pop(ind)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"message": f"postid {id} was not found"})

@app.put("/posts/{id}")
def put_post(id: int, upd_post: Post):
    post_dict = upd_post.dict()
    ind = find_index_post(id)
    #print(id, ind , my_posts)
    if ind is not None:
        post_dict['id'] = id
        my_posts[ind] = post_dict
        return Response(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"message": f"postid {id} was not found"})



if __name__ == "__main__":
    upd_post = Body({"title":"Beaches in Florida", "content":"Awesome beaches from Florida", "id":1})
    #a = put_post(1, upd_post)


