# Simple makefile to make working with project easier

V_PIP := venv/bin/pip3
V_PYTHON := venv/bin/python3
V_PYTEST:= venv/bin/py.test
APP_PORT := 6606

run-refresher: # refresh offers for products
	env REFRESHER_CONFIG='./confs/productator.conf.json' $(V_PYTHON) -m productator.refresher

run-api: # run api
	env PRODUCTATOR_CONFIG='./confs/productator.conf.json' FLASK_APP='productator/api' FLASK_RUN_PORT=$(APP_PORT) FLASK_ENV=development venv/bin/flask run

bootstrap: # create environment for running / developing
	pip3 install virtualenv
	python3 -m venv venv --clear
	$(V_PIP) install -r requirements.txt -r test-requirements.txt

tests: # run tests
	docker-compose down
	docker-compose run -d --publish 3306:3306 db
	sleep 20 # give mysql some time to start up
	$(V_PYTEST) $(CURDIR)/productator/tests/
	docker-compose down

