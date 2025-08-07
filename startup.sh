cd /home/site/wwwroot

python manage.py collectstatic --noinput

exec gunicorn StarInTheKitchen.wsgi:application --bind=0.0.0.0