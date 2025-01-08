import sqlalchemy
from databases import Database
from dynaconf import settings

metadata = sqlalchemy.MetaData()


async def db_connection() -> Database:
    database_url = f"postgresql+asyncpg://{settings['DB_USERNAME']}:"
    database_url += f"{settings['DB_PASSWORD']}@"
    database_url += f"{settings['DB_HOST']}:5432/"
    database_url += f"{settings['DATABASE_NAME']}"
    database = Database(database_url, min_size=5, max_size=20)

    return database
