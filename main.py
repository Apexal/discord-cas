import os
from flask import Flask, g, session, request, render_template, redirect, url_for
from flask_cas import CAS, login_required, logout
from dotenv import load_dotenv

from discord import OAUTH_URL, VERIFIED_ROLE_ID, get_tokens, get_user_info, add_user_to_server, add_role_to_member, set_member_nickname

# Load .env into os.environ
load_dotenv()

app = Flask(__name__)
cas = CAS(app, '/cas')

app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.config['CAS_SERVER'] = 'https://cas-auth.rpi.edu/cas'
app.config['CAS_AFTER_LOGIN'] = '/'


@app.route('/')
@login_required
def index():
    return f'<a href="{OAUTH_URL}">Connect Discord</a>'


@app.route('/discord/callback', methods=['GET'])
@login_required
def discord_callback():
    # Extract code or error from URL
    authorization_code = request.args.get('code')
    error = request.args.get('error')

    # Exchange authorization code for tokens
    tokens = get_tokens(authorization_code)

    # Get info on the Discord user that just connected (really only need id)
    discord_user = get_user_info(tokens['access_token'])

    nickname = 'Placeholder Nickname'

    # Add them to the server
    add_user_to_server(tokens['access_token'], discord_user['id'], nickname)

    # Set their nickname
    set_member_nickname(discord_user['id'], nickname)

    # Give them the verified role
    add_role_to_member(discord_user['id'], VERIFIED_ROLE_ID)

    return tokens['access_token']
