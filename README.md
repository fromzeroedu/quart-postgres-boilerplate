# Quart Postgres Boilerplate

![Code Check](https://github.com/fromzeroedu/quart-postgres-boilerplate/workflows/Code%20Checks/badge.svg)

This is a boilerplate for a Postgres Quart app that can run as a local poetry-based, Heroku or Docker application. Requires `python 3.7` or higher.

## Local Development

### Install Poetry

- Install Poetry if you don't have it using `pip install poetry`
    - On WSL install using the get-poetry route. For example, on Ubuntu, do `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -`. 
- Install the packages: `poetry install`
- To open a Quart shell, just do `poetry run quart shell`

### First Migration

- Run the first migration with `poetry run alembic upgrade head`
  - Subsequent migrations after models changes can be run with `poetry run alembic revision --autogenerate -m "added app table field"` with [some caveats](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect).

### Running the application

- To run the application do: `poetry run quart run`
- Open `http://localhost:5000` on your browser

### Run Tests

- Run tests by doing `poetry run pytest`

## Using Docker

- Make sure your folder is being shared within Docker client (Preferences > Resources > File Sharing)
- Run `docker-compose up --build`. If there's a timeout error, you can restart the Quart container.
- To do the first migration:
  - `docker-compose run --rm web poetry run alembic upgrade head`
- Restart using docker-compose and head over to `http://localhost:5000` on your browser
- Run tests by doing `docker-compose run --rm web poetry run pytest -s`
- To connect to the Docker PostgreSQL shell, do `docker exec -it app_db_1 psql postgres -U app_user`

## Production

- Use Hypercorn `hypercorn --bind 0.0.0.0:$PORT --reload wsgi:app`

## Codespaces

- Start the Codespace
- First time:
  - Run `poetry install`
  - Restart VSCode for changes to be applied
  - After restart:
    - Make sure to select the poetry Python interpreter for VSCode
    - Do the first migration: `poetry run alembic upgrade head`
- To run the application: `poetry run quart run`
  - The codespace will give you a private URL for your application
- To connect to Postgres Database: `psql -h localhost -Uapp_user postgres`
