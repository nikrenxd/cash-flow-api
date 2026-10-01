DC = docker compose

DC_ARGS ?= --env-file .env -f docker/compose.yaml
DC_DEV_ARGS ?= --env-file .env.dev -f docker/compose-dev.yaml

.PHONY: migrations migrate run-local run-web run-dinfra run-infra run-worker down

migrations:
	python cash_flow/manage.py makemigrations

migrate:
	python cash_flow/manage.py migrate

run-local:
	DJANGO_ENV=development python cash_flow/manage.py runserver

run-worker:
	celery -A cash_flow.root worker --loglevel=info

dev-infra:
	${DC} $(DC_DEV_ARGS) up

run-web:
	${DC} $(DC_ARGS) up web

run-infra:
	${DC} $(DC_ARGS) up worker database redis rabbitmq

down:
	${DC} $(DC_ARGS) down

build:
	${DC} $(DC_ARGS) build --no-cache
