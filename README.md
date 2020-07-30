# Producator 4000
Productator is an API for storing and managing products and offers. <br>
Productator uses an external [API](​https://applifting.herokuapp.com/api/v1) for collecting and updating offers. 

## Main parts of producator
Productator consists of two main parts that make all the magic.<br>
`Productator API` - allows access for managing and viewing product and their offers <br>
`Refresher JOB` - runs every minute to refresh product offers from external API

### API
It's a simple Flask api. In production it uses UWSGI to run properly. <br>
By default runs on port `6606` <br>
Everything needed is ready to be deployed in docker image.

### Refresher
It's a small script downloading offers from remote api every 30 seconds by default <br>
Everything needed is ready to be deployed in docker image.

## Endpoints
All endpoints with examples can be found at [endpoints readme](ENDPOINTS.md).

## Dependencies
### Software
```bash
 - Python3
 - Python3-pip
```
### Services
```bash
 - MySQL database with imported dump
 - Running external Offers API
```
## Used python packages
These packages are used to run API correctly: 
```bash
- Flask
- Flask-SQLAlchemy
- requests
- PyMySQL
```

## Running it locally
There is a `Makefile` provided to make developing and running easier. <br> 
First make sure you have all stuff from `Dependecies` section installed. <br>
After checking you are safe to run `make bootstrap` command that will prepare 
developing environment and install all packages. <br>
All parts of `productator` can be all run at once by using `docker-compose up` 
or can be run separately using steps bellow:

### Productator Database
All `productator` parts require a MySQL database to run properly. To start it use
`docker-compose run --publish 3306:3306 db`.

### Productator API
After bootstraping all the packages, you can run `make run-api` to start the API <br>

### Offer refresher job
Refresher has the same requirements as `productator API` so there is no need to install anything else. <br>
To run `refresher` use command `make refresh`

## Tests
Ouh yeah, we have some tests. It's mix of unit and integration tests. <br>
Simply run `make tests`

## Overriding using ENV variables
If you have a need to override some config stuff using environment variables here is a list of whats possible.
```BASH
API
- PRODUCTATOR_CONFIG = path to config file
- OFFERS_MS_ADDRESS = base address to the external offers service
- DATABASE_HOST = hostname of the database server

REFRESHER
- REFRESHER_CONFIG = path to the config file
- DATABASE_HOST = hostname of the database server
- REFRESHER_PERIOD = delay until next offer check (by default its 30 seconds)
```

## Possible updates
Here are some possible future changes / features to be made
```bash
- Refresher uses models from API 
- Metrics on endpoint /metrics
- Liveness and Readiness endpoints for kubernetes
- Kubernetes manifests to run in kube cluster
- User authentification to access API
- Swagger
- Tracking histoy of offers
```


### NOTE
Everything is commented, so if you wont find something in README it will be visible in files right away <br>
If you have any questions please contact us.

TOTAL DEV TIME: 3 md
