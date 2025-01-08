from dynaconf import settings
from quart import Blueprint

home_app = Blueprint("home_app", __name__)


@home_app.route("/app-settings")
async def app_settings() -> str:
    """
    The home page for a home type
    """

    return (
        "<h3>Home: Hello World!</h3>"
        + f"<p>Dynaconf Environment: {settings.ENV_FOR_DYNACONF}</br>"  # type: ignore
        + f"DB_HOST: {settings.DB_HOST}</p>"  # type: ignore
    )
