from fastapi import HTTPException, Response, Depends, APIRouter, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from typing import List
from .. import utils, database, models, oauth2, schemas

from datetime import datetime

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if the email already exists in the database
    query = db.query(models.User).filter(models.User.email == user.email)
    if query.first() != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The {user.email} email is already exist!!!")
        

    # Hash the user's password
    user.password = await utils.hash(user.password)
    
    # Create a new User instance with the provided user details
    user = models.User(**user.dict())
    
    # Add the user to the database
    db.add(user)
    
    # Commit the changes to the database
    db.commit()
    
    # Refresh the user object to ensure that the object in memory is up-to-date with the database
    db.refresh(user)
    
    # Return the user object
    return user

@router.put("/update", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
async def update_user(updated_user: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Check if the updated email already exists in the database
    query = db.query(models.User).filter(models.User.email == updated_user.email)
    if query.first() != None and updated_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The {updated_user.email} email is already exist!!!")
        
    # Hash the updated password
    updated_user.password = await utils.hash(updated_user.password)

    # Retrieve the current user from the database
    user = db.query(models.User).filter(models.User.id == current_user.id)
    
    # Update the current user's details with the updated user details
    user.update(updated_user.dict(), synchronize_session=False)
    
    # Commit the changes to the database
    db.commit()
    
    # Return the updated user object
    return user.first()

@router.post('/token', response_model=schemas.Token, summary="Generate Token")
async def token(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Query the user by email
    user = db.query(models.User).filter(models.User.email == user_credentials.username)

    # Check if user exists in database
    if not user.first():
        raise HTTPException(status_code=404, detail=f"User with {user_credentials.username} email is not exist")
    
    # Verify user's password
    verify = await utils.verify(user_credentials.password, user.first().password)

    # Raise error if verification failed
    if not verify:
        raise HTTPException(status_code=403, detail=f"Invalid Credentials")

    # Create access token with user_id payload
    access_token = await oauth2.create_access_token(data={"user_id": user.first().id})

    # Update user's last_login time in database
    user.update({"last_login": datetime.now()}, synchronize_session = False)
    db.commit()

    # Return access token
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserReturn)
async def current_user(current_user: int = Depends(oauth2.get_current_user)):
    # Return the current user from the token payload
    return current_user


