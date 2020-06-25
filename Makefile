PYTHON = python3.8
ENV = env
PYBIN = $(ENV)/bin
PIP = $(PYBIN)/pip


.PHONY: default-setup
default-setup: check ensure-local-db test

.PHONY: help
help:
	@echo "make                       # Prepare (virtualenv, pip install, run dbs, migrations, format, lint and run tests)"
	@echo "make run                   # (Prepare and) Launch local app"
	@echo "make test                  # (Prepare and) Run tests"
	@echo "make createsuperuser       # (Prepare and) Create admin user"
	@echo "make makemigrations        # (Prepare and) Make migrations"
	@echo "make cleanup-local-db      # (Prepare and) Cleanup and restart local db"

$(ENV)/.virtual-env-created:
	virtualenv -p $(PYTHON) $(ENV)
	touch $(ENV)/.virtual-env-created

$(ENV)/.pip-install-done: $(ENV)/.virtual-env-created requirements.txt
	$(PIP) install -r requirements.txt
	touch $(ENV)/.pip-install-done

.PHONY: check
check: $(ENV)/.pip-install-done

	# Black code formatter first:
	$(PYBIN)/black menuratings

	# Flake8 linter after that:
	$(PYBIN)/flake8 menuratings

.PHONY: test
test: check
	# Tests and coverage:
	$(PYBIN)/pytest --cov . --cov-report html:htmlcov --exitfirst

.PHONY: ensure-local-db
ensure-local-db: $(ENV)/.pip-install-done

	# Ensure local db is started:
	docker-compose -f ./docker/local_dbs/docker-compose.yml up -d

	# Wait till it's ready
	$(PYBIN)/python3 docker/local_dbs/wait.py
	
	# Run migrations
	$(PYBIN)/python3 manage.py migrate

.PHONY: run
run: default-setup
	$(PYBIN)/python3 manage.py runserver

.PHONY: createsuperuser
createsuperuser: default-setup
	$(PYBIN)/python3 manage.py createsuperuser

.PHONY: makemigrations
makemigrations: $(ENV)/.pip-install-done
	$(PYBIN)/python3 manage.py makemigrations

.PHONY: cleanup-local-db
cleanup-local-db:

	# Stop, remove and restart local db:
	docker-compose -f ./docker/local_dbs/docker-compose.yml stop
	docker-compose -f ./docker/local_dbs/docker-compose.yml rm

	# Start again:
	make ensure-local-db

	# Create super user:
	make createsuperuser