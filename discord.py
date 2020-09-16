import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_BASE = 'https://discordapp.com/api'
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
CLIENT_ID = os.environ.get('DISCORD_CLIENT_ID')
CLIENT_SECRET = os.environ.get('DISCORD_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('DISCORD_REDIRECT_URI')
HEADERS = {
    'Authorization': 'Bot ' + DISCORD_BOT_TOKEN,
}


def get_tokens(code):
    '''Given an authorization code, request the access and refresh tokens for a Discord user. Returns the tokens. Throws an error if invalid request.'''
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
