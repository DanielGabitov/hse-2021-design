import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.endpoints import authorization, classes

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv('MIDDLEWARE_SECRET'))

app.include_router(authorization.auth_router)
app.include_router(classes.classes_router)
