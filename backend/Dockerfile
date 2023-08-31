FROM python:3.11-alpine

ENV POETRY_VERSION=1.6.1

WORKDIR /app

# COPY requirements.txt .
# RUN pip install --upgrade pip --no-cache-dir
# RUN pip install -r requirements.txt --no-cache-dir

RUN pip install poetry==$POETRY_VERSION
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --without dev

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "garage.wsgi"]
