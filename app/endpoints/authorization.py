import os
import requests

from fastapi import APIRouter, Depends, Request, Response
from starlette.responses import RedirectResponse

from app.helpers.github_interactions import get_user_email, get_user_info
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
    scope = 'user:email'
    redirect_uri = 'http://localhost:80/authorization/'
    return RedirectResponse(url=f'https://github.com/login/oauth/authorize?'
                                f'client_id={client_id}&'
                                f'scope={scope}&'
                                f'redirect_uri={redirect_uri}')

# @auth_router.get('/')
# async def authorize(request: Request, response: Response, db=Depends(setup.get_db)):
#     return []
# token = await oauth.github.authorize_access_token(request)
# github_auth_response = await oauth.github.get('user', token=token)
#
# profile = github_auth_response.json()
# github_login = profile['login']
# access_token = token['access_token']
# nickname = profile['name']
#
# if crud.get_user(db=db, github_login=github_login) is None:
#     email = await get_user_email(github_login=github_login, access_token=access_token)
#     crud.create_user(db=db, github_login=profile['login'], nickname=nickname, email=email)
#
# response.set_cookie(key='username', value=github_login)
# response.set_cookie(key='access_token', value=access_token)
#
# return response


@auth_router.get('/')
async def authorize(code: str, response: Response, db=Depends(setup.get_db)):
    client_id = os.getenv('GITHUB_CLIENT_ID')
    client_secret = os.getenv('GITHUB_CLIENT_SECRET')
    auth_response = requests.post(url=f'https://github.com/login/oauth/access_token?'
                                      f'client_id={client_id}&'
                                      f'client_secret={client_secret}&'
                                      f'code={code}').text

    token = extract_token(auth_response)
    github_login, nickname, email = get_user_info(access_token=token)

    if crud.get_user(db=db, github_login=github_login) is None:
        crud.create_user(db=db, github_login=github_login, nickname=nickname, email=email)

    response.set_cookie(key='username', value=github_login)
    response.set_cookie(key='access_token', value=token)
    return github_login, nickname, email
    # return response
