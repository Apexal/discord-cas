import os
from flask import Flask, g, session, request, render_template, redirect, url_for
from flask_cas import CAS, login_required, logout
import urllib.parse
from dotenv import load_dotenv

from discord import OAUTH_URL, VERIFIED_ROLE_ID, SERVER_ID, get_tokens, get_user_info, get_member, add_user_to_server, add_role_to_member, set_member_nickname
import requests

# Load .env into os.environ
load_dotenv()

app = Flask(__name__)
cas = CAS(app, '/cas')

app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.config['SITE_TITLE'] = os.environ.get('SITE_TITLE')
app.config['CAS_SERVER'] = 'https://cas-auth.rpi.edu/cas'
app.config['CAS_AFTER_LOGIN'] = '/'


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        user = {
            'name': dict()
        }
        app.logger.info(f'Home page requested by {cas.username}')
        return render_template('join.html', user=user, rcs_id=cas.username.lower())
    elif request.method == 'POST':
        # Limit to 20 characters so overall Discord nickname doesn't exceed limit of 32 characters
        first_name = request.form['first_name'].strip()[:20]
        last_name = request.form['last_name'].strip()
        graduation_year = request.form['graduation_year'].strip()[2:]

        name = first_name + ' ' + last_name[0]
        # TODO: persist nickname somewhere else to avoid changing it
        nickname = f'{name} \'{graduation_year} ({cas.username.lower()})'
        app.logger.info(f'Redirecting {cas.username} to Discord OAuth page')
        return redirect(OAUTH_URL + '&state=' + urllib.parse.quote(nickname))


@app.route('/discord/callback', methods=['GET'])
@login_required
def discord_callback():
    # Extract code or error from URL
    authorization_code = request.args.get('code')
    error = request.args.get('error')

    if error:
        # Handle the special case where the user declined to connect
        if error == 'access_denied':
            app.logger.error(
                f'{cas.username} declined to connect their Discord account')
            return render_template('error.html', error='You declined to connect your Discord account!')
        else:
            # Handle generic Discord error
            error_description = request.args.get('error_description')
            app.logger.error(
                f'An error occurred on the Discord callback for {cas.username}: {error_description}')
            raise Exception(error_description)

    # Extract nickname from state parameter
    nickname = request.args.get('state')

    # Exchange authorization code for tokens
    tokens = get_tokens(authorization_code)

    session['tokens'] = tokens

    # Get info on the Discord user that just connected (really only need id)
    discord_user = get_user_info(tokens['access_token'])
    session['discord_user_id'] = discord_user['id']

    # Add them to the server
    add_user_to_server(tokens['access_token'], discord_user['id'], nickname)
    app.logger.info(f'Added {cas.username} to Discord server')

    # Set their nickname
    try:
        set_member_nickname(discord_user['id'], nickname)
        app.logger.info(
            f'Set {cas.username}\'s nickname to "{nickname}" on server')
    except requests.exceptions.HTTPError as e:
        app.logger.warning(
            f'Failed to set nickname "{nickname}" to {cas.username} on server: {e}')

    # Give them the verified role
    try:
        add_role_to_member(discord_user['id'], VERIFIED_ROLE_ID)
        app.logger.info(f'Added verified role to {cas.username} on server')
    except requests.exceptions.HTTPError as e:
        app.logger.warning(
            f'Failed to add role to {cas.username} on server: {e}')

    return render_template('joined.html', rcs_id=cas.username.lower(), nickname=nickname, discord_server_id=SERVER_ID)


@app.errorhandler(Exception)
def handle_error(e):
    app.logger.exception(e)

    # Hide error in production
    error = e
    if app.env == 'production' and not e.name == 'Not Found':
        error = 'Something went wrong... Please try again later.'

    return render_template('error.html', error=error), 500
