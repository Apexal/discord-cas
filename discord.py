'''Methods to interact with Discord API. 

Only a small subset of API endpoints are accounted for here.
Based on the Discord API Documentation https://discord.com/developers/docs/intro
'''

from http.client import responses
import os
from typing import Dict, List
import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError
load_dotenv()

API_BASE = 'https://discordapp.com/api'

# Environment variables (all required)
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
CLIENT_ID = os.environ.get('DISCORD_CLIENT_ID')
CLIENT_SECRET = os.environ.get('DISCORD_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('DISCORD_REDIRECT_URI')

# Authorization header with the bot token that allows us to do everything
HEADERS = {
    'Authorization': 'Bot ' + BOT_TOKEN,
}


# The url users are redirected to to initiate the OAuth2 flow
BOT_JOIN_URL = f'https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&permissions=134217730&redirect_uri={REDIRECT_URI}&scope=bot'
OAUTH_URL = f'https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=guilds.join%20identify'


def get_tokens(code):
    '''
    Given an authorization code, request the access and refresh tokens for a Discord user.
    Returns the tokens. Throws an error if invalid request.

    Discord docs: https://discord.com/developers/docs/topics/oauth2
    '''
    response = requests.post(f'{API_BASE}/oauth2/token',
                             data={
                                 'client_id': CLIENT_ID,
                                 'client_secret': CLIENT_SECRET,
                                 'grant_type': 'authorization_code',
                                 'code': code,
                                 'redirect_uri': REDIRECT_URI,
                                 'scope': 'identity guilds.join'
                             },
                             headers={
                                 'Content-Type': 'application/x-www-form-urlencoded'
                             }
                             )
    response.raise_for_status()
    tokens = response.json()
    return tokens


def refresh_tokens(refresh_token):
    response = requests.post(f'{API_BASE}/oauth2/token',
                             data={
                                 'client_id': CLIENT_ID,
                                 'client_secret': CLIENT_SECRET,
                                 'grant_type': 'refresh_token',
                                 'refresh_token': refresh_token,
                                 'redirect_uri': REDIRECT_URI,
                                 'scope': 'identity guilds.join'
                             },
                             headers={
                                 'Content-Type': 'application/x-www-form-urlencoded'
                             }
                             )
    response.raise_for_status()
    tokens = response.json()
    return tokens


def get_user_info(access_token):
    '''
    Given an access token, get a Discord user's info including id, username, discriminator, avatar url, etc.
    Throws an error if invalid request.

    Discord docs: https://discord.com/developers/docs/resources/user#get-current-user
    '''
    response = requests.get(f'{API_BASE}/users/@me', headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    )
    response.raise_for_status()
    user = response.json()
    return user

def get_user(user_id: str) -> Dict:
    response = requests.get(
        f'{API_BASE}/users/{user_id}', headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_member(server_id: str, user_id: str) -> Dict:
    '''
    Retreive a server member. Includes the user, their server nickname, roles, etc.

    Discord docs: https://discord.com/developers/docs/resources/guild#get-guild-member
    '''
    response = requests.get(
        f'{API_BASE}/guilds/{server_id}/members/{user_id}', headers=HEADERS)
    try:
        response.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 404:
            return None
        raise e

    return response.json()


def add_user_to_server(server_id: str, access_token: str, user_id: str, nickname: str, verified_role_ids: List[str]):
    '''
    Given a Discord user's id, add them to the Discord server with their nickname
    set as their RCS ID and with the verified role.

    Discord docs: https://discord.com/developers/docs/resources/guild#add-guild-member
    '''
    response = requests.put(f'{API_BASE}/guilds/{server_id}/members/{user_id}',
                            json={
                                'access_token': access_token,
                                'nick': nickname,
                                'roles': verified_role_ids,
                            },
                            headers=HEADERS
                            )
    response.raise_for_status()
    return response


def kick_member_from_server(server_id: str, user_id: str):
    '''
    Remove a member from the server.

    Discord docs: https://discord.com/developers/docs/resources/guild#remove-guild-member
    '''
    response = requests.delete(
        f'{API_BASE}/guilds/{server_id}/members/{user_id}', headers=HEADERS)
    response.raise_for_status()
    return response


def set_member_nickname(server_id: str, user_id: str, nickname: str):
    '''
    Given a Discord user's id, set their nickname on the server.

    Discord docs: https://discord.com/developers/docs/resources/guild#modify-guild-member
    '''
    response = requests.patch(f'{API_BASE}/guilds/{server_id}/members/{user_id}',
                              json={
                                  'nick': nickname
                              },
                              headers=HEADERS
                              )
    response.raise_for_status()
    return response


def add_role_to_member(server_id: str, user_id: str, role_id: str):
    '''
    Add a role (identified by its id) to a member.

    Discord docs: https://discord.com/developers/docs/resources/guild#add-guild-member-role
    '''
    response = requests.put(
        f'{API_BASE}/guilds/{server_id}/members/{user_id}/roles/{role_id}', headers=HEADERS)
    response.raise_for_status()
    return response


def remove_role_from_member(server_id: str, user_id: str, role_id: str):
    '''
    Remove a role (identified by its id) from a member.

    Discord docs: https://discord.com/developers/docs/resources/guild#remove-guild-member-role
    '''
    response = requests.delete(
        f'{API_BASE}/guilds/{server_id}/members/{user_id}/roles/{role_id}', headers=HEADERS)
    response.raise_for_status()
    return response
