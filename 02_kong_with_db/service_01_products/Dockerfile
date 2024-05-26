FROM python:3.12-slim

WORKDIR /app/

COPY . /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install


CMD ["poetry", "run", "uvicorn", "products.main:app", "--host", "0.0.0.0", "--port", "8002"]