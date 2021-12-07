import os
import requests

from fastapi import APIRouter, Depends, Response, HTTPException
from starlette.responses import RedirectResponse

from app.helpers.github_interactions import get_user_info
from app.database import setup, crud

auth_router = APIRouter(
    prefix='/authorization'
)


# auth_data ~ access_token=example_token&scope=example_scope&token_type=bearer
def extract_token(auth_data: str):
    return auth_data.split('&')[0].split('=')[1]


@auth_router.get('/login')
async def login():
    client_id = os.getenv('GITHUB_CLIENT_ID')
    scope = 'user:email repo delete_repo'
    redirect_uri = 'http://localhost:8000/authorization/'
    return RedirectResponse(url=f'https://github.com/login/oauth/authorize?'
                                f'client_id={client_id}&'
                                f'scope={scope}&'
                                f'redirect_uri={redirect_uri}')


# todo handle denied request to login
@auth_router.get('/')
async def authorize(code: str, response: Response, db=Depends(setup.get_db)):
    client_id = os.getenv('GITHUB_CLIENT_ID')
    client_secret = os.getenv('GITHUB_CLIENT_SECRET')
    auth_response = requests.post(url=f'https://github.com/login/oauth/access_token?'
                                      f'client_id={client_id}&'
                                      f'client_secret={client_secret}&'
                                      f'code={code}')

    if auth_response.status_code != 200:
        raise HTTPException(status_code=500, detail='could not get access token')

    token = extract_token(auth_response.text)
    username, email = get_user_info(access_token=token)

    response.set_cookie(key='username', value=username)
    response.set_cookie(key='access_token', value=token)

    if crud.get_user(db=db, username=username) is None:
        crud.create_user(db=db, username=username, email=email)
        return f'User <{username}> has been successfully signed UP'

    # printing token is NOT safe but its here now for debug convenience
    return f'User <{username}> with access_token = <{token}> has been successfully signed IN'
