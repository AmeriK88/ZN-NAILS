# 1 Generar migraciones, migrar y recoger estáticos
release: sh -c "python manage.py makemigrations --noinput \
    && python manage.py migrate --noinput \
    && python manage.py collectstatic --noinput"

# 2 Arrancar Gunicorn usando el puerto que Railway inyecta
web: gunicorn zemar_nails.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --log-file -
