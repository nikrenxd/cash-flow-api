DC = docker compose

.PHONY: migrations migrate run-local run-container run-infra

migrations:
	python src/cash_flow/manage.py makemigrations

migrate:
	python src/cash_flow/manage.py migrate

run-local:
	python src/cash_flow/manage.py runserver

run-container:
	docker compose up web

run-infra:
	docker compose up worker database redis rabbitmq