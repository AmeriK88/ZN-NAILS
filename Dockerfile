########################
# 1) Build stage
########################
FROM python:3.13.5-slim-bookworm AS builder


# Dependencias de compilación (solo aquí)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
        libmariadb-dev-compat \
        libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Compilamos wheels offline para copiar solo binarios
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

COPY . .

########################
# 2) Runtime stage
########################
FROM python:3.13.5-slim-bookworm AS runtime


# Parcheamos el sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends libmariadb3 && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalamos dependencias ya compiladas
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copiamos el código
COPY --from=builder /app /app
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=zemar_nails.settings

EXPOSE 8080

CMD ["sh", "-c", "\
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    exec gunicorn zemar_nails.wsgi:application \
      --bind 0.0.0.0:${PORT:-8080} \
      --workers 3 \
      --log-level info \
      --access-logfile - \
"]
