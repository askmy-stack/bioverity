from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Engine


def database_healthy(engine: Engine) -> bool:
    with engine.connect() as connection:
        connection.execute(text("SELECT postgis_version()"))
        connection.execute(text("SELECT 1 FROM observations LIMIT 1"))
    return True
