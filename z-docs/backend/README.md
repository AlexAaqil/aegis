# Aegis Backend
Aegis is a fraud detection application.

This service is built with Django + DRF + Celery + Postgres and managed using poetry for dependency management.

## Basic Setup
To set up the Aegis backend:
- Clone the repo and go into /aegis/backend.
- Ensure Python 3.11+ and Poetry are installed.
- Run ```poetry install```
- Run the server with ```poetry run uvicorn app.main:app --reload```
- Visit http://127.0.0.1:8000/health

## Prerequisites
Make sure you have the following installed:
- Python 3.11 (required)
- Poetry (dependency manager)
    ```
    pip install poetry
    ```

Create a virtual environment with poetry and attach python version to be used
```
poetry init --no-interaction \
  --name aegis-backend \
  --description "Aegis backend — offline biometric + rule-based fraud detection (MVP)" \
  --author "Your Team <you@example.com>" \
  --python="^3.10"
```

Install dependencies
```
poetry add fastapi uvicorn[standard] sqlmodel pydantic cryptography python-multipart pillow numpy
```
What these are for:
- fastapi — lightweight typed API framework.
- uvicorn[standard] — ASGI server to run the app.
- sqlmodel — ORM (SQLModel = Pydantic + SQLAlchemy).
- pydantic — data validation / settings.
- cryptography — encrypt biometric data & logs.
- python-multipart — support multipart file uploads.
- pillow — image handling.
- numpy — numeric ops (embeddings, similarity).


To recreate the environment and install dependecies:
```
poetry install
```

Run the app (should run at https://localhost:8000)
```
poetry run python manage.py migrate
poetry run uvicorn app.main:app --reload
```

Create a superuser
```
poetry run python manage.py createsuperuser
```

## Configurations
In the .env file, change CORS_ALLOWED_ORIGINS to the front end dev server URL.

## Workings
[User initiates transaction] → [Stored in DB] → [Fraud check] → [Risk score + Alert if risky]