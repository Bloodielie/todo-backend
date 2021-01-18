FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app
COPY ./alembic.ini .
COPY ./alembic /alembic