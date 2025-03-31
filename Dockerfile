FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .
COPY existence_check.py .

RUN poetry install --no-root 

CMD ["python3","existence_check.py"]