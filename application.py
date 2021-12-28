from quart import Quart

from db import db_connection


def create_app(**config_overrides):
    app = Quart(__name__)

    # Load config
    app.config.from_pyfile("settings.py")

    # apply overrides for tests
    app.config.update(config_overrides)

    # import blueprints
    from counter.views import counter_app

    # register blueprints
    app.register_blueprint(counter_app)

    @app.before_serving
    async def create_db_conn():
        database = await db_connection()
        await database.connect()
        app.dbc = database

    @app.after_serving
    async def close_db_conn():
        await app.dbc.disconnect()

    return app
