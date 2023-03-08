# Import pydantic BaseSettigns module.
from pydantic import BaseSettings

# Define the Settings class which inherits from BaseSettings
class Settings(BaseSettings):
    # Define properties corresponding to environment variables
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    
    app_version: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    username: str
    password: str



    # Define the Config inner class with the path to the environment file
    class Config:
        env_file = ".env"

# Define the title of the FastAPI Starter Project API
title = "📌 FastAPI Starter Project"

# Define the description of the FastAPI Starter Project API
description = """
FastAPI Starter API Project helps you do awesome stuff. 🚀 \n
This app is a FastAPI starter project. ❗️ \n
Provides a basic configuration for building RESTful APIs. 💯 \n
Includes settings for following: 📍\n
    🔷  Connecting to a PostgreSQL database \n
    🔷  Sets up authentication using bcrypt hashing \n
    🔷  Defines endpoints for user authentication \n
    🔷  Code is designed to be easily extensible and customizable \n
    🔷  Ideal for developers who want to get up and running quickly with a solid foundation for their FastAPI application \n
"""

# Define the tags for the FastAPI Starter Project API
tags_metadata = [
    {
        "name": "Auth",
        "description": "Login and logout logic is here",
    },
    {
        "name": "Users",
        "description": "Only for Admin: Operations with users.",
    },
]

# Create an instance of the Settings class
settings = Settings()
