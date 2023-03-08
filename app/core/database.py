# Import necessary modules from SQLAlchemy and project-specific modules.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Form the database URL from the settings provided
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Create the database engine using the URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a declarative base for the models
Base = declarative_base()

# Create a session maker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    # Create a new session
    db = SessionLocal()
    try:
        # Yield the session to be used by the caller
        yield db
    finally:
        # Close the session when done
        db.close()
