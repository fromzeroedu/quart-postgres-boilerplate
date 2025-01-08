from sqlalchemy import Column, Integer, Table

from my_app.db import metadata

counter_table = Table(
    "counter",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("count", Integer),
)
