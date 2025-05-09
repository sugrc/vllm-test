FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .
COPY realism_evaluation_system.py .

RUN poetry install --no-root 

CMD ["python3","realism_evaluation_system.py"]