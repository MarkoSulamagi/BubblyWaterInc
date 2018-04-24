# Bubbly Water Inc.

A small programming exercise. Assignment can be found [here](assignment.pdf).

## Assumptions about assignment

- One meter measures only hot or cold water. Not both together.
- Content of meter reading is following:
`{
  "meter_id": "6769f62ffd987be1592fba44b0daab59",
  "type": "HOT|COLD",
  "measured_at": 1523952169,  # Unix Epoc time
  "value": 200,
  "battery": 49  # percentage
}`
- No load tests (keeping it out of scope this time)
- Dashboard interface:
    - No registration or authentication, forgot password, profile edit or new user creation
    - Total daily consumption for all meters
    - Dashboard for single customers:
    - Daily consumptions for single customer
    - Current battery info for meters on customer view
- If there's some kind of disturbance when adding new readings (say power disconnect) then that's not handled in the solution.



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
docker exec -it bubblywater_api python -m unittest tests





