docker-compose down -v
docker-compose up -d --build
docker-compose exec api python manage.py makemigrations tournament
docker-compose exec api python manage.py migrate --no-input
docker-compose exec api python manage.py initadmin
