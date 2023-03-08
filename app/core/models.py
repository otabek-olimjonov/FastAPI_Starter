# Import necessary modules from SQLAlchemy for defining database schema
from sqlalchemy import Column, Integer, Float, Boolean, String, ForeignKey, DateTime

# Import necessary functions from SQLAlchemy for defining relationships between tables
from sqlalchemy.orm import relationship

# Import necessary functions from SQLAlchemy for using built-in SQL functions
from sqlalchemy.sql import func

# Import necessary modules from datetime for storing timestamps in the database
from datetime import datetime

# Import the Base class from the database module for defining database tables
from .database import Base


# Define User model with SQLAlchemy ORM
class User(Base):
    # Set the table name for this model
    __tablename__ = "users"

    # Define the columns for this model
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50),  nullable=False) # user's name
    email = Column(String(50), unique=True, nullable=False, index=True) # user's email, unique
    password = Column(String(256), nullable=False) # user's password, required and not nullable

    verified = Column(Boolean, nullable=False, server_default='False')

    role = Column(String(10), server_default='user', nullable=False)

    last_login = Column(DateTime, server_default=func.now()) # the datetime of the user's last login
    created_at = Column(DateTime, server_default=func.now()) # the datetime of when the user was created
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now()) # the datetime of when the user was last updated
