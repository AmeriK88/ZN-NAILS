# 1) Build stage: instalar dependencias y compilar assets
FROM python:3.13.1-slim AS build

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       default-libmysqlclient-dev \
       pkg-config \
       libmariadb-dev-compat \
       libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# 2) Runtime stage: sólo lo imprescindible
FROM python:3.13.1-slim

WORKDIR /app

# Copiar dependencias y código
COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=build /app /app

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=zemar_nails.settings

EXPOSE 8000

CMD ["sh", "-c", "\
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn zemar_nails.wsgi:application --bind 0.0.0.0:8000 \
"]
