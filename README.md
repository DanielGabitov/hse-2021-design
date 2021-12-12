### ToDo proper ReadMe

### How to run
run containers
```
docker compose build
docker compose up -d
```
run migrations
```
docker exec -it app bash
pipenv run alembic upgrade head
```
####url: `localhost:80`