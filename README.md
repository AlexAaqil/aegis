# Aegis Backend
Aegis is a fraud detection application.

This service is built with Django + DRF + Celery + Postgres and managed using poetry for dependency management.

## Prerequisites
Make sure you have the following installed:
- Python 3.12 (required)
- Poetry (dependency manager)
    ```
    pip install poetry
    ```

Create a virtual environment with poetry
```
poetry env user python 3.12
```
Install dependencies
```
poetry install
```
Run the app (should run at https://localhost:8000)
```
poetry run python manage.py migrate
poetry run python manage.py runserver
```

## Configurations
In the .env file, change CORS_ALLOWED_ORIGINS to the front end dev server URL.