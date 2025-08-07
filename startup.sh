cd /home/site/wwwroot

celery -A StarInTheKitchen worker --loglevel=info &

python manage.py collectstatic --noinput

exec gunicorn StarInTheKitchen.wsgi:application --bind=0.0.0.0