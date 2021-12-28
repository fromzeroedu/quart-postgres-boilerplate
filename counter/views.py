from quart import Blueprint, current_app, Response

from counter.models import counter_table

counter_app = Blueprint("counter_app", __name__)


@counter_app.route("/")
async def init() -> str:
    conn = current_app.dbc  # type: ignore
    counter_query = counter_table.select()
    result = await conn.fetch_all(query=counter_query)
    count = None

    if not len(result):
        stmt = counter_table.insert().values(count=1)
        result = await conn.execute(stmt)
        await conn.execute("commit")
        count = 1
    else:
        row = result[0]
        count = row["count"] + 1
        counter_update = counter_table.update(
            counter_table.c.id == row["id"]
        ).values({"count": count})
        result = await conn.execute(counter_update)
        await conn.execute("commit")
    return "<h1>Counter: " + str(count) + "</h1>"
