from fastapi import FastAPI, Response, status, Depends, HTTPException, Response, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, Schemas, utils, models, oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model = Schemas.Token)
#def login(user_credentials: Schemas.UserLogin, db: Session = Depends( database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends( database.get_db)):
    userdb = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not userdb:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"User {user_credentials.username} not found")
    if not utils.Verify(user_credentials.password, userdb.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id": userdb.id})
    return {"access_token": access_token, "token_type": "bearer"}



