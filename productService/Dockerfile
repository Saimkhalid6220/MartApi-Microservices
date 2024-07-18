FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY . /code/

RUN poetry config virtualenvs.create false

RUN poetry install 

EXPOSE 8001

CMD ["poetry", "run", "uvicorn", "productservice.main:app", "--host", "0.0.0.0", "--port", "8001","--reload"]