# Import from passlib.contetxt CryptContext module.
from passlib.context import CryptContext
from . import models
from fastapi import status, HTTPException

# Initialize the password context with the bcrypt hashing scheme
# and set "deprecated" to "auto" to automatically upgrade to a newer algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def hash(password: str):
    """
    Hashes a password using the initialized password context.

    Args:
    - password (str): The plain-text password to hash.

    Returns:
    - str: The hashed password string.
    """
    return pwd_context.hash(password)

async def verify(plain_password, hashed_password):
    """
    Verifies a plain-text password against a hashed password string.

    Args:
    - plain_password (str): The plain-text password to verify.
    - hashed_password (str): The hashed password string to compare against.

    Returns:
    - bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


