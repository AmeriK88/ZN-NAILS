# Aplica migraciones y recoge estáticos en cada deploy
release: python manage.py migrate collectstatic --noinput

# Arranca Gunicorn apuntando a tu WSGI y escuchando en el puerto que Railway te da
web: gunicorn zemar_nails.wsgi:application --bind 0.0.0.0:$PORT --log-file -
