from typing import AsyncGenerator

import pytest
from dynaconf import settings
from quart import Quart
from quart.typing import TestClientProtocol
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from typing_extensions import Never

from my_app.application import create_app
from my_app.db import metadata
from my_app.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture
async def create_db() -> AsyncGenerator[dict, Never]:
    if settings.ENV_FOR_DYNACONF == "DEVELOPMENT":
        settings.configure(FORCE_ENV_FOR_DYNACONF="TESTING")
    if settings.ENV_FOR_DYNACONF == "DOCKER":
        settings.configure(FORCE_ENV_FOR_DYNACONF="DOCKER_TESTING")
    if settings.ENV_FOR_DYNACONF == "DEVCONTAINER":
        settings.configure(FORCE_ENV_FOR_DYNACONF="DEVCONTAINER-TESTING")

    db_test_uri = "postgresql://%s:%s@%s:5432/%s" % (
        settings["DB_USERNAME"],
        settings["DB_PASSWORD"],
        settings["DB_HOST"],
        settings["DATABASE_NAME"],
    )

    # Log the key application configuration like database connection
    logger.info(f"Testing Environment: {settings['ENV_FOR_DYNACONF']}")
    logger.info(f"Testing Database URI: {db_test_uri}")

    # drop the database if it exists
    if database_exists(db_test_uri):
        logger.info(f"Dropping Database URI: {db_test_uri}")
        drop_database(db_test_uri)

    # create test database
    logger.info(f"Creating Database URI: {db_test_uri}")
    create_database(db_test_uri)

    yield {
        "DB_TEST_URI": db_test_uri,
    }

    logger.info(f"Dropping Testing Database URI: {db_test_uri}")

    # create new engine to drop test database
    drop_database(db_test_uri)


@pytest.fixture
async def create_test_app(create_db: dict[str, str]) -> AsyncGenerator[Quart, None]:
    logger.info("Setting up test app")
    app = await create_app()

    # Create engine and create all tables
    engine = create_engine(create_db["DB_TEST_URI"])
    metadata.create_all(engine)

    # Start the dabaase connection
    await app.startup()

    yield app

    logger.info("Tearing down test app")

    # Stop the database connection
    await app.shutdown()

    # Clean up
    metadata.drop_all(engine)


@pytest.fixture
def create_test_client(create_test_app: Quart) -> TestClientProtocol:
    logger.info("Creating test client")
    return create_test_app.test_client()
