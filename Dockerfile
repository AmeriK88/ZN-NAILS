# 1) Build stage: instalar dependencias
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

# Copia paquetes y proyecto
COPY --from=build /usr/local /usr/local
COPY --from=build /app /app

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=zemar_nails.settings

# Railway inyecta el puerto correcto en $PORT (8080)
EXPOSE 8080

# Antes de arrancar Gunicorn, migramos y recogemos estáticos
CMD ["sh", "-c", "\
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    exec gunicorn zemar_nails.wsgi:application \
      --bind 0.0.0.0:$PORT \
      --workers 3 \
      --log-level debug \
      --access-logfile - \
"]
