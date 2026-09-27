from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Engine


def database_healthy(engine: Engine) -> bool:
    with engine.connect() as connection:
        connection.execute(text("select 1"))
    return True
