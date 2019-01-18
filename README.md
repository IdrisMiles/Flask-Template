# Dockerized Flask App Template

This is a simple template for a dockerized flask app with google oauth, it is intended to be a useful starting point for future projects.

## Requirements

 - Docker
 - docker-compose

## How to run

Check out the repo:

```bash
git clone https://github.com/IdrisMiles/Flask-Template.git
```

Run the flask app in a docker container
```bash
# change into project dir
cd Flask-Template

# build the docker container
sudo docker-compose build

# run flask app in docker container
sudo docker-compose up
```
