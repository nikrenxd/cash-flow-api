## Running the Project

### Running via docker-compose

To run the project, you will need to have Docker and Docker Compose installed on your device.
The project is launched using the Makefile commands

#### For local environment:

```shell
make up
```

#### For prod environment:

To launch project on VPS, you will need to do few steps before run it

1. Move and rename .env file from environments directory to root

```shell
mv environments/.env.example . && mv .env.example .env
```

2. Run project in dev mode and collect static files, after that kill containers

```shell
docker compose up -d
docker compose exec web-app python manage.py collectstatic
docker compose down
```

3. Now we can run our project

```shell
docker compose -f docker-compose.prod.yml up
```

### After launching project

After you launch project, create database tables

```shell
docker compose exec web-app python manage.py migrate
```

Creating database tables for prod environment

```shell
docker compose exec -f docker-compose.prod.yml web-app python manage.py migrate
```

### Tests

To run tests simply use Makefile command while app is running via Docker:

```shell
make test
```