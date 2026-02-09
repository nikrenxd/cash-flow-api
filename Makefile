DC = docker compose

.PHONY: migrations migrate

migrations:
	python src/cash_flow/manage.py makemigrations

migrate:
	python src/cash_flow/manage.py migrate

run-local:
	python src/cash_flow/manage.py runserver
