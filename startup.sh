cd /home/site/wwwroot/StarInTheKitchen

if [ -d "../antenv" ]; then
  source ../antenv/bin/activate
fi

exec gunicorn StarInTheKitchen.wsgi:application --bind=0.0.0.0
