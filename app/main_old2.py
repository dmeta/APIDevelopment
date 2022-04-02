#para executar o webserver: uvicorn app.main2:app --reload
import psycopg2
from psycopg2.extras import RealDictConnection, RealDictCursor
import os
import urllib.parse as up
from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.exceptions import HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


try:
    url = "postgres://zevlzacq:DT3nExkM6ueKUSXPAwyaxT7XtBpgJ1W8@raja.db.elephantsql.com/zevlzacq"
    url = up.urlparse(url)
    conn = psycopg2.connect(database=url.path[1:],user=url.username, password=url.password, host=url.hostname, port=url.port, 
                            cursor_factory=RealDictCursor)
    
    # Open a cursor to perform database operations
    cursor = conn.cursor()
    
    # Execute a command: this creates a new table
    cursor.execute("SELECT * FROM public.post LIMIT 100")
    for row in cursor:
        print (row)
        
    # Retrieve query results
    cursor.execute("SELECT * FROM public.post LIMIT 100")
    records = cursor.fetchall()
    print (records )
    #conn.commit()
    #cursor.close()
    #conn.close()
    print("OK: Connection to database succesfully")
except Exception as error:
    print("ERROR: Connection to database failure: ", error)


app = FastAPI()
my_posts=[{"title":"Beaches in Florida", "content":"Awesome beaches from Florida", "id":1}, {"title":"the grand cook book", "content":"best receipts", "id":2}]
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int] = None



@app.get("/")
def root():
    return "API Development"

@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    cursor.execute("SELECT * FROM public.post")
    records = cursor.fetchall()
    return {"data": records}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_postss(post: Post):
    post_dict = post.dict()

    cursor.execute(f""" insert into post (title, content, published) values (%s, %s, %s) RETURNING * """ , 
                   (post_dict['title'], 
                    post_dict['content'], 
                    post_dict['published']))
    new_post = cursor.fetchone()
    conn.commit()
    print ("new_post: ", new_post)

    #my_posts.append(post_dict)
    return {"data": new_post}


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int, response: Response):
    print ("id***************************: ", id, str(id))
    cursor.execute(f""" select * from post where id = %s """ , (str(id), )) ## important last colon to avoid string conversion error
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"message": f"postid {id} was not found"})
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"postid {id} was not found"}
    return {"post detail": f"post {post}"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(f""" delete from post where id = %s RETURNING * """ , (str(id), )) ## important last colon to avoid string conversion error
    post = cursor.fetchone()
    conn.commit()
    print (post)
    if post:
    #    my_posts.pop(ind)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"message": f"postid {id} was not found"})





@app.put("/posts/{id}")
def put_post(id: int, upd_post: Post):
    cursor.execute(f""" update post set title = %s, content = %s, published = %s where id = %s RETURNING * """ , 
                   (upd_post.title, 
                   upd_post.content, 
                   upd_post.published, 
                   str(id), )) ## important last colon to avoid string conversion error
    post = cursor.fetchone()
    conn.commit()
    print (post)
    if post:
    #    my_posts.pop(ind)
        return Response(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"message": f"postid {id} was not found"})







