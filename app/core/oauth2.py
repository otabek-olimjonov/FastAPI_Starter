from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials

from . import schemas, database, models
from .config import settings

import secrets

# Define OAuth2 security scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

# Load secret key and algorithm from settings file
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

# Define the number of minutes before access tokens expire
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Create a HTTPBasic security object to use in the get_swagger_access function
security = HTTPBasic()


async def create_access_token(data: dict):
    """Create a JWT access token based on user data"""
    # Make a copy of the data dictionary to avoid modifying the original
    to_encode = data.copy()

    # Calculate the expiration time of the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add the expiration time to the data dictionary
    to_encode.update({"exp": expire})

    # Encode the data as a JWT access token using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def verify_access_token(token: str, credentials_exception):
    """Verify the authenticity of a JWT access token"""
    try:
        # Decode the access token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Get the user ID from the decoded payload
        id: str = payload.get("user_id")

        # Raise an exception if the user ID is missing or invalid
        if id is None:
            raise credentials_exception

        # Create a TokenData object with the user ID
        token_data = schemas.TokenData(id=id)
    except JWTError:
        # Raise an exception if the access token cannot be decoded or is invalid
        raise credentials_exception

    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """Get the current user based on a JWT access token"""
    # Define an exception to raise if the access token is missing or invalid
    credentials_exception = HTTPException(status_code=401, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # Verify the authenticity of the access token
    token = await verify_access_token(token, credentials_exception)

    # Get the user from the database based on the user ID in the access token
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

async def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """Get the current admin user based on a JWT access token"""
    user = await get_current_user(token, db)
    if user.role == 'admin':
        return user
    raise HTTPException(status_code=401, detail=f"User is not admin", headers={"WWW-Authenticate": "Bearer"})


async def get_swagger_access(credentials: HTTPBasicCredentials = Depends(security)):
    """Authenticate Swagger UI access using HTTP basic authentication"""
    # Check that the username and password are correct
    correct_username = secrets.compare_digest(credentials.username, settings.swagger_username)
    correct_password = secrets.compare_digest(credentials.password, settings.swagger_password)
    if not (correct_username and correct_password):
        # Raise an exception if the credentials are incorrect
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    # Return the username as a string if the credentials are correct
    return credentials.username
