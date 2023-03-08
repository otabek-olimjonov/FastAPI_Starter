# Import necessary modules from FastAPI and project-specific modules.
from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from typing import List
from .core import models, database, routers, oauth2
from .core.config import settings, description, title, tags_metadata

# Create a new FastAPI instance and set its properties.
app = FastAPI(
    title=title,  # Set the title of the app to the value of the `title` variable.
    description=description,  # Set the description of the app to the value of the `description` variable.
    version=settings.app_version,  # Set the version of the app to the value of the `app_version` variable in the `settings` module.
    terms_of_service="https://intrepid.uz",  # Set the terms of service URL for the app.
    docs_url=None,  # Disable the default "/docs" endpoint.
    redoc_url=None,  # Disable the default "/redoc" endpoint.
    openapi_url = None,  # Disable the default "/openapi.json" endpoint.
)

# Include the router defined in the `routers` module in the app.
app.include_router(routers.router)

# Set the allowed origins for CORS requests.
origins = [
    "*"
]

# Add a CORS middleware to the app.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables from the metadata defined in the `models` module.
# models.Base.metadata.create_all(bind=database.engine)

# Define an endpoint for retrieving the Swagger UI documentation.
@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(oauth2.get_swagger_access)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

# Define an endpoint for retrieving the ReDoc documentation.
@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(oauth2.get_swagger_access)):
    return get_redoc_html(openapi_url="/openapi.json", title="docs")

# Define an endpoint for retrieving the OpenAPI specification document.
@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(oauth2.get_swagger_access)):
    return get_openapi(
        title=app.title +  " - Swagger UI",
        description=app.description,
        version=app.version,
        terms_of_service=app.terms_of_service,
        routes=app.routes,
        tags=tags_metadata
    )
