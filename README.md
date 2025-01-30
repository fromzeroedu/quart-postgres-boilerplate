# Quart-Feed

## Setup
You need to run alembic migrations the first time you run the app. 

To do this, start the app with the following command:
```bash
docker-compose up --build -d
```

Then, run the following command to run the migrations:  
```bash
docker-compose exec web poetry run alembic upgrade head
```

## Running tests

To run the tests, run the following command:
```bash
docker-compose --profile testing run --rm test poetry run pytest
```

## Debugging locally

To ensure compatibility with Python version on Docker locally, install Poetry packages pinning to the Python 3.10 version as follows:
```bash
poetry env use python3.10 && poetry install
```

If you don't have Python 3.10 installed, you can install it using `pyenv`:
```bash
pyenv install 3.10.0
```

See the Pyenv documentation for more information on how to install it.
