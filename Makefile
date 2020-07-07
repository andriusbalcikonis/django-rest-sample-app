PYTHON = python3.8
ENV = env
PYBIN = $(ENV)/bin
PIP = $(PYBIN)/pip
PIP_COMPILE = $(PYBIN)/pip-compile


.PHONY: default-setup
default-setup: check ensure-local-db test

.PHONY: help
help:
	@echo "make                       # Prepare (virtualenv, pip install, run dbs, file server, graylog, run migrations, format, lint and run tests)"
	@echo "make run                   # (Prepare and) Launch local app"
	@echo "make test                  # (Prepare and) Run tests"
	@echo "make createsuperuser       # (Prepare and) Create admin user"
	@echo "make makemigrations        # (Prepare and) Make migrations"
	@echo "make stop-services         # (Prepare and) Stop local services (dbs, file server, graylog)"
	@echo "make upgrade-requirements  # (Prepare and) Upgrade used python packages"
	

$(ENV)/.virtual-env-created:
	# Set up virtualenv
	virtualenv -p $(PYTHON) $(ENV)

	# Install pip-tools, it will help to manage requirements.txt, which will contain all other requirements
	$(PIP) install pip-tools  

	touch $(ENV)/.virtual-env-created

requirements.txt: $(ENV)/.virtual-env-created
	$(PIP_COMPILE) requirements.in -o requirements.txt

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
	docker-compose -f ./docker/docker-compose.development.yml up -d

	# Wait till it's ready
	$(PYBIN)/python3 docker/wait.py
	
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

.PHONY: make stop-local-services
make stop-local-services:
	docker-compose -f ./docker/docker-compose.development.yml stop

.PHONY: upgrade-requirements
upgrade-requirements: $(ENV)/.pip-install-done

	# Remove requirements.txt:
	rm requirements.txt

	# Generate requirements.txt from requirements.in:
	$(PIP_COMPILE) requirements.in -o requirements.txt