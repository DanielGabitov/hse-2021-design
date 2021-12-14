
### How to run
1) Set env variables from the list:
```
DATABASE_URL=,
GITHUB_CLIENT_ID=,
GITHUB_CLIENT_SECRET=,
MIDDLEWARE_SECRET=
```

2) Run containers
```
docker compose build
docker compose up -d
```
3) Run migrations
```
docker exec -it app bash
pipenv run alembic upgrade head
```
4) You are awesome

#### url: `localhost:80`
