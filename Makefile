PYTHON = python3.8
ENV = env
PYBIN = $(ENV)/bin
PIP = $(PYBIN)/pip


.PHONY: default
default: ensure-local-db

.PHONY: help
help:
	@echo "make                     # Ensure ready (virtualenv, pip install, run dbs, migrations)"
	@echo "make run                 # (Ensure ready and) Launch local app"
	@echo "make createsuperuser     # (Ensure ready and) Create admin user"

$(ENV)/.virtual-env-created:
	virtualenv -p $(PYTHON) $(ENV)
	touch $(ENV)/.virtual-env-created

$(ENV)/.pip-install-done: $(ENV)/.virtual-env-created requirements.txt
	$(PIP) install -r requirements.txt
	touch $(ENV)/.pip-install-done

.PHONY: ensure-local-db
ensure-local-db: $(ENV)/.pip-install-done

	# Ensure local db is started:
	docker-compose -f ./docker/local_dbs/docker-compose.yml up -d

	# Wait till it's ready
	$(PYBIN)/python3 docker/local_dbs/wait.py
	
	# Run migrations
	$(PYBIN)/python3 manage.py migrate

.PHONY: run
run: ensure-local-db
	$(PYBIN)/python3 manage.py runserver

.PHONY: createsuperuser
createsuperuser: ensure-local-db
	$(PYBIN)/python3 manage.py createsuperuser
