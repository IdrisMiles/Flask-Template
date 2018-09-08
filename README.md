# Dockerized Flask App Template

This is a simple template for a dockerized flask app with google oauth, it is intended to be a useful starting point for future projects.

## Requirements

 - Docker
 - docker-compose

## How to run

Check out the repo:

```bash
git clone https://github.com/IdrisMiles/dockerized_flask.git
```

Run the flask app in a dicker container
```bash
# change into project dir
cd dockerized_flask

# build the docker container
sudo docker-compose build

# run flask app in docker container
sudo docker-compose up
```
