After docker containers are running
docker exec -it bubblywater_api python manage.py db init
docker exec -it bubblywater_api python manage.py db migrate
docker exec -it bubblywater_api python manage.py db upgrade

docker exec -it bubblywater_reactapp npm install --save redux

docker exec -it bubblywater_api python -m unittest tests.py



# Seed database
docker exec -it bubblywater_api python manage.py seed

# Purge database
docker exec -it bubblywater_api python manage.py purge