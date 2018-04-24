Steps to run the application in development:
# Clone the project
`git clone git@github.com:MarkoSulamagi/BubblyWaterInc.git`

# Install docker
https://docs.docker.com/install/
Ubunut 16.04 https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04

# Install docker-compose
https://docs.docker.com/compose/
Ubuntu 16.04 https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-16-04

# Build application
`docker-compose build`
Docker needs to download all the dependencies, so it could take a while.

# Run application
`docker-compose up`
Docker needs to download all the dependencies, so it could take a while. 
Depending on the speed of the internet. Downloads only happen on first run. 

# Run DB migrations
`docker exec -it bubblywater_api python manage.py db init`
`docker exec -it bubblywater_api python manage.py db migrate`
`docker exec -it bubblywater_api python manage.py db upgrade`

# Seed database
docker exec -it bubblywater_api python manage.py seed

Visit http://localhost:3333

# Purge database
docker exec -it bubblywater_api python manage.py purge

After docker containers are running

# During development
# Install new JS library
docker exec -it bubblywater_reactapp npm install --save redux

# Run API unit tests
docker exec -it bubblywater_api python -m unittest tests.py





