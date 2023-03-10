## FastAPI Starter Project

```
├── app
│   ├── core
│   │   ├── api
│   │   │   ├── auth.py
│   │   │   └── users.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── oauth2.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── utils.py
│   └── main.py
├── migrations
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── 
├── .env
├── docker-compose.yml
├── Dockerfile
├── prestart.sh
├── README.md
├── alembic.ini
└── requirements.txt
```

# Setting up the project without Docker

1. Clone the repository from GitHub.
    ```
    git clone https://github.com/Otabek0626/FastAPI_Starter.git
    ```

2. Enter the cloned project folder.
    ```
    cd FastAPI_Starter
    ```

3. Create a virtual environment using Python's `venv` module:

    ```
    python -m venv .venv
    ```
    or
    ```
    python3 -m venv .venv
    ```

4. Activate the virtual environment:

    - For Windows:

        ```
        .venv\Scripts\activate.bat
        ```

    - For Linux or macOS:

        ```
        source .venv/bin/activate
        ```

5. Install the required dependencies using `pip`:

    ```
    pip install -r requirements.txt
    ```

5. Create a database using pgadmin. ex: `fastapi_starter`

6. Update `.env` file with your own values.
    ```
    ## Databse Credentials
    DATABASE_HOSTNAME=localhost
    DATABASE_PORT=5432
    DATABASE_PASSWORD=password
    DATABASE_NAME=fastapi_starter
    DATABASE_USERNAME=postgres

    ## App settings
    APP_VERSION=1.0.0
    SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=100

    ## Swagger credentials
    USERNAME=user
    PASSWORD=pass
    ```




7. Set up the database using alembic by running the following command:
    - makemigrations
        ```
        alembic revision --autogenerate -m "initial"
        ```
    - migrate
        ```
        alembic upgrade head
        ```

8. Start the server:

    ```
    uvicorn app.main:app --reload
    ```

8. Navigate to http://localhost:8000/docs to see the Swagger UI and interact with the API. 
    `Note`: the Swagger credentials are in `.env` file


# Setting up the project with Docker

1. Clone the repository from GitHub.
    ```
    git clone https://github.com/Otabek0626/FastAPI_Starter.git
    ```

2. Enter the cloned project folder.
    ```
    cd FastAPI_Starter
    ```

3. Build the docker compose:
    ```
    docker-compose up --build -d
    ```

4. Open the fastapi container terminal and then make migrations.
    - makemigrations
        ```
        alembic revision --autogenerate -m "initial"
        ```
    - migrate
        ```
        alembic upgrade head
        ```

5. Navigate to http://localhost:8000/docs to see the Swagger UI and interact with the API. 
    `Note`: the Swagger credentials are in `.env` file