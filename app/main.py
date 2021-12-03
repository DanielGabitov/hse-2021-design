import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.endpoints import authorization

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv('MIDDLEWARE_SECRET'))

app.include_router(authorization.auth_router)
