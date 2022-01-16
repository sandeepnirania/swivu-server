# Make commands for development
# 
# `make requirements.flag` install required Python modules.
# `make build` generates required migrations.
# `make run` runs the server, listening on port 8000.

PIP=pip
PYTHON=python

requirements.txt: requirements.in
	$(PIP) install -r requirements.in
	echo "# GENERATED FROM requirements.in.  DO NOT EDIT DIRECTLY." > requirements.txt
	$(PIP) freeze >> requirements.txt

requirements.flag: requirements.txt
	$(PIP) install -r requirements.txt
	touch requirements.flag

build: requirements.flag
	$(PYTHON) ./manage.py makemigrations

test: build
	$(PYTHON) ./manage.py test

run: build
	$(PYTHON) ./manage.py migrate
	$(PYTHON) ./manage.py runserver

graphiql:
	open http://localhost:8000/graphql/
