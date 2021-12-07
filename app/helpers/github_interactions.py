import requests
from fastapi import HTTPException

from app.schemas.class_schema import ClassCreate
from app.helpers.auth_setup import AuthInfo


def get_user_email(*, username: str, access_token: str):
    response = requests.get(
        url=f'https://api.github.com/user/emails',
        headers={'Authorization': f'token {access_token}'}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500,
                            detail=f'Could not fetch email for {username}')

    email = None
    for elem in response.json():
        if elem['primary']:
            email = elem['email']

    if email is None:
        raise HTTPException(status_code=400,
                            detail=f'User <{username}> does not have primary email')
    return email


# todo async
def get_user_info(*, access_token: str):

    response = requests.get(url='https://api.github.com/user', headers={'Authorization': f'token {access_token}'})
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail='could not fetch user info')

    response = response.json()
    username = response['login']
    email = get_user_email(username=username, access_token=access_token)

    return username, email


def create_repo(*, auth_info: AuthInfo, class_: ClassCreate):
    response = requests.post(url='https://api.github.com/user/repos',
                             headers={'Authorization': f'token {auth_info.access_token}'},
                             json={'name': class_.name})
    if response.status_code != 201:
        raise HTTPException(status_code=500,
                            detail=f'could not create <{class_.name}> class for <{auth_info.user.username}>')
    return response.json()['html_url']


def delete_repo(*, auth_info: AuthInfo, class_name: str):
    response = requests.delete(url=f'https://api.github.com/repos/{auth_info.user.username}/{class_name}',
                               headers={'Authorization': f'token {auth_info.access_token}'})
    if response.status_code != 204:
        raise HTTPException(status_code=500,
                            detail=f'could not delete <{class_name}> class for <{auth_info.user.username}>')


def get_repo(*, auth_info: AuthInfo, class_name: str):
    response = requests.get(url=f'https://api.github.com/repos/{auth_info.user}/{class_name}')
    if response.status_code == 404:
        return None
    if response.status_code == 200:
        return response.json()['html_url']
    raise HTTPException(status_code=500,
                        detail=f'could not get repo <{class_name}> for user <{auth_info.user}>')
