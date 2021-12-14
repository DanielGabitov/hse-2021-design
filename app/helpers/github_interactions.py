import requests
from typing import Optional, Tuple, NoReturn
from fastapi import HTTPException

from app.schemas.class_schema import ClassCreate
from app.helpers.auth_setup import AuthInfo


def get_user_email(*, username: str, access_token: str) -> str:
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
        raise HTTPException(
            status_code=400,
            detail=f'User <{username}> does not have primary email'
        )
    return email


# todo (5) async
def get_user_info(*, access_token: str) -> Tuple[str, str]:

    response = requests.get(url='https://api.github.com/user',
                            headers={'Authorization': f'token {access_token}'})
    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail='could not fetch user info'
        )

    response = response.json()
    username = response['login']
    email = get_user_email(username=username, access_token=access_token)

    return username, email


def create_repo(*, auth_info: AuthInfo, class_: ClassCreate) -> str:
    response = requests.post(
        url='https://api.github.com/user/repos',
        headers={'Authorization': f'token {auth_info.access_token}'},
        json={'name': class_.name, "auto_init": True}
    )
    if response.status_code != 201:
        raise HTTPException(
            status_code=500,
            detail=f'could not create <{class_.name}> class for '
                   f'<{auth_info.user.username}>. response: {response.content}'
        )
    return response.json()['html_url']


# todo (6) throwing HTTP exception out of these functions is not a good idea
def delete_repo(*, auth_info: AuthInfo, class_name: str) -> NoReturn:
    response = requests.delete(
        url=f'https://api.github.com/'
            f'repos/{auth_info.user.username}/{class_name}',
        headers={'Authorization': f'token {auth_info.access_token}'})
    if response.status_code != 204:
        raise HTTPException(
            status_code=500,
            detail=f'could not delete <{class_name}> '
                   f'class for <{auth_info.user.username}>'
        )


# todo (9) these methods should be independent from main app logic
#  (no auth, class_name -> repo_name etc)
def get_repo(*, auth_info: AuthInfo, class_name: str) -> Optional[str]:
    response = requests.get(
        url=f'https://api.github.com/repos/{auth_info.user}/{class_name}')
    if response.status_code == 404:
        return None
    if response.status_code == 200:
        return response.json()['html_url']
    raise HTTPException(
        status_code=500,
        detail=f'could not get repo <{class_name}> for user <{auth_info.user}>'
    )


def get_branch_last_commit(owner: str, repo: str,
                           branch_name: str = 'main') -> str:
    response = requests.get(
        url=f'https://api.github.com/repos/'
            f'{owner}/{repo}/branches/{branch_name}')
    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f'could not get <{owner}/{repo}> repo last '
                   f'commit for branch {branch_name}'
        )
    return response.json()['commit']['sha']


def create_branch(owner: str, repo: str, branch_name: str,
                  access_token: str, commit_sha: str) -> NoReturn:
    response = requests.post(
        url=f'https://api.github.com/repos/{owner}/{repo}/git/refs',
        headers={'Authorization': f'token {access_token}'},
        json={'ref': f'refs/heads/{branch_name}', 'sha': commit_sha}
    )

    if response.status_code != 201:
        raise HTTPException(
            status_code=500,
            detail=f'could not create branch <{branch_name}> for '
                   f'<{owner}/{repo}> repo on commit <{commit_sha}>'
        )


def delete_branch(owner: str, repo: str, branch_name: str,
                  access_token: str) -> NoReturn:
    response = requests.delete(
        url=f'https://api.github.com/repos/{owner}/{repo}/git/'
            f'refs/heads/{branch_name}',
        headers={'Authorization': f'token {access_token}'},
    )

    if response.status_code != 204:
        raise HTTPException(
            status_code=500,
            detail=f'could not delete branch <{branch_name}> for '
                   f'<{owner}/{repo}> repo'
        )
