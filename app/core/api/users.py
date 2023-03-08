from fastapi import HTTPException, Response, Depends, APIRouter, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from .. import utils, database, models, oauth2, schemas

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_admin)):
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

@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
async def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_admin)):
    # Check if the updated email already exists in the database
    query = db.query(models.User).filter(models.User.email == updated_user.email)
    if query.first() != None and updated_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The {updated_user.email} email is already exist!!!")
        
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

@router.get("/{id}", response_model=schemas.UserReturn)
async def get_user(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_admin)):
    # Check if the updated email already exists in the database
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=404, detail=f"The {id} is not found!!!")
    
    # Return the updated user object
    return user

@router.get("/", response_model=List[schemas.UserReturn])
async def get_users(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_admin)):
    # Check if the updated email already exists in the database
    users = db.query(models.User).all()
    
    # Return the updated user object
    return users


@router.delete("/{id}", response_model=schemas.UserReturn)
async def get_user(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_admin)):
    # Check if the updated email already exists in the database
    query = db.query(models.User).filter(models.User.id == id)
    user = query.first()
    if user == None:
        raise HTTPException(status_code=404, detail=f"The {id} is not found!!!")
    
    # Delete and commit
    query.delete()
    db.commit()

    # Return the updated user object
    return user


