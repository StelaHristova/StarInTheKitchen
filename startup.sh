cd /home/site/wwwroot

if [ -d .venv ]; then
  source .venv/bin/activate
fi

if [ -f .env ]; then
  export $(cat .env | xargs)
fi

#celery -A StarInTheKitchen worker --loglevel=info --detach

python manage.py collectstatic --noinput

exec gunicorn StarInTheKitchen.wsgi:application --bind=0.0.0.0