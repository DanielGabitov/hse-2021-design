FROM python:3.8
WORKDIR /code

# Install dependencies via pipenv
COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock
COPY ./wait-for /code/wait-for
RUN pip install pipenv
RUN pipenv install --ignore-pipfile --deploy

# Copy project
COPY app /code/app

# Copy alembic
COPY alembic /code/alembic
COPY alembic.ini /code/alembic.ini

# Copy env
COPY .env /code

# Install netcat for wait-for
RUN apt-get -q update && apt-get -qy install netcat

# Run fastapi app with wait-for tool
# See what wait-for does: https://github.com/eficode/wait-for
# todo (7) download wait-for from git repo
CMD ["sh", "-c", "./wait-for database:5432 -- pipenv run uvicorn app.main:app --host 0.0.0.0 --port 80"]
