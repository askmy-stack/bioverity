FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md alembic.ini ./
COPY backend/ ./backend/
COPY migrations/ ./migrations/
COPY policies/ ./policies/

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn bioverity.api.main:app --host 0.0.0.0 --port 8000 --app-dir backend"]
