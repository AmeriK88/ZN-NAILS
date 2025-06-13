# 1) Build stage: instalar dependencias, compilar assets y recoger estáticos
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

# Instala requisitos
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia el código
COPY . .

# Usa tu settings y recopila estáticos
ENV DJANGO_SETTINGS_MODULE=zemar_nails.settings
RUN mkdir -p /app/staticfiles \
    && python manage.py collectstatic --noinput

# 2) Runtime stage: solo lo imprescindible
FROM python:3.13.1-slim

WORKDIR /app

# Copia paquetes y proyecto
COPY --from=build /usr/local /usr/local
COPY --from=build /app /app

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=zemar_nails.settings

# Railway inyecta el puerto correcto en $PORT (8080)
EXPOSE 8080

# Arranca Gunicorn
CMD ["gunicorn", "zemar_nails.wsgi:application", \
     "--bind", "0.0.0.0:$PORT", \
     "--workers", "3", \
     "--log-level", "debug", \
     "--access-logfile", "-"]
