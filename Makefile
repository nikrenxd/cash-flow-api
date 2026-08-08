DC = docker compose

DC_ARGS ?= --env-file .env -f docker/docker-compose.yml

.PHONY: migrations migrate run-local run-web run-infra run-worker down

migrations:
	python cash_flow/manage.py makemigrations

migrate:
	python cash_flow/manage.py migrate

run-local:
	python cash_flow/manage.py runserver

run-worker:
	celery -A cash_flow.root worker --loglevel=info

run-web:
	${DC} $(DC_ARGS) up web

run-infra:
	${DC} --env-file .env -f docker/docker-compose.yml up worker database redis rabbitmq

down:
	${DC} --env-file .env -f docker/docker-compose.yml down

build:
	${DC} --env-file .env -f docker/docker-compose.yml build --no-cache
