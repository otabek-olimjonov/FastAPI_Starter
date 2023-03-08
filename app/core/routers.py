# Import necessary modules from FastAPI and project-specific modules.
from fastapi import APIRouter
from .api import auth, users

# Create an API router with the prefix "/api"
router = APIRouter(prefix="/api")

# Mount the authentication sub-router at the "/auth" endpoint
# and tag it with "Auth"
router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Auth"],
)

# Mount the users sub-router at the "/users" endpoint
# and tag it with "Users"
router.include_router(
    users.router, 
    prefix="/users", 
    tags=["Users"],
)
