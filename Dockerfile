FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV ARANDU_USE_MOCK=true
ENV ARANDU_DEBUG=false

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
