import requests
from fastapi import HTTPException


def get_user_email(*, github_login: str, access_token: str):
    response = requests.get(
        url=f'https://api.github.com/user/emails',
        headers={'Authorization': f'token {access_token}'}
    ).json()
    for elem in response:
        if elem['primary']:
            return elem['email']
    return None


# todo async
def get_user_info(*, access_token: str):
    r = requests.get(url='https://api.github.com/user', headers={'Authorization': f'token {access_token}'})
    r = r.json()
    github_login = r['login']
    nickname = r['name']
    email = get_user_email(github_login=github_login, access_token=access_token)
    if email is None:
        raise HTTPException(status_code=500, detail='could not fetch user email')
    return github_login, nickname, email
