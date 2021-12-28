from sqlalchemy import Table, Column, Integer

from db import metadata

counter_table = Table(
    "counter",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("count", Integer),
)
