cd /home/site/wwwroot

if [ -d "../.venv" ]; then
  source ../.venv/bin/activate
fi

python manage.py collectstatic --noinput

exec gunicorn StarInTheKitchen.wsgi:application --bind=0.0.0.0