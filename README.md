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
│       └── 685e742a7975_initial.py
├── .env
├── docker-compose.yml
├── Dockerfile
├── README.md
├── alembic.ini
└── requirements.txt

# Setting up the project

1. Clone the repository from GitHub.

2. Create a virtual environment using Python's `venv` module:

    ```
    python -m venv .venv
    ```

3. Activate the virtual environment:

    - For Windows:

        ```
        .venv\Scripts\activate.bat
        ```

    - For Linux or macOS:

        ```
        source .venv/bin/activate
        ```

4. Install the required dependencies using `pip`:

    ```
    pip install -r requirements.txt
    ```

5. Create a `.env` file based on the provided `.env.example` file and update it with your own values.

6. Set up the database by running the following command:

    ```
    alembic upgrade head
    ```

7. Start the server:

    ```
    uvicorn app.main:app --reload
    ```

8. Navigate to http://localhost:8000/docs to see the Swagger UI and interact with the API.
