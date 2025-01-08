from typing import Any

from dynaconf import settings
from quart import Quart

from my_app.counter_app.views import counter_app
from my_app.db import db_connection
from my_app.home_app.views import home_app
from my_app.logger import get_logger

logger = get_logger(__name__)


def init_config(app: Quart, **config_overrides: Any) -> None:
    """Initialize configuration"""
    app.config.from_object(settings)
    app.config.update(config_overrides)


async def create_app(**config_overrides: Any) -> Quart:
    """
    Factory application creator
    args: config_overrides = testing overrides
    """
    logger.info("Creating application")
    app = Quart(__name__)
    init_config(app, **config_overrides)

    # register blueprints
    app.register_blueprint(home_app)
    app.register_blueprint(counter_app)

    # Log the key application configuration like database connection, env_for_dynaconf
    logger.info(f"App Environment: {app.config['ENV_FOR_DYNACONF']}")
    logger.info(f"App Database Host: {app.config['DB_HOST']}")
    logger.info(f"App Database Name: {app.config['DATABASE_NAME']}")

    @app.before_serving
    async def create_db_conn() -> None:
        database = await db_connection()
        await database.connect()
        app.dbc = database  # type: ignore

    @app.after_serving
    async def close_db_conn() -> None:
        await app.dbc.disconnect()  # type: ignore

    return app
