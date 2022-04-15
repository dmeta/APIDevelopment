from os import error
from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import Schemas, database, models, oauth2

router = APIRouter(prefix = "/vote", tags = ['Vote'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def get_votes(vote: Schemas.Vote, db: Session = Depends(database.get_db), 
              current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    print ("query: ", vote_query )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"User {current_user.id} has already voted on that post {vote.post_id}" )
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        try:
            db.add(new_vote)
            db.commit()
        except BaseException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post {vote.post_id} does not exist. Error: {err}")
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail= f"Vote for post {vote.post_id} was added")
        #return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Vote for post {vote.post_id} doesnt exist")
        vote_query.delete (synchronize_session=False)
        db.commit()

        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail= f"Vote for post {vote.post_id} was deleted")
        
        #return {"message": "Successfully deleted vote"}
