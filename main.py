import os
import redis
import json
from flask import Flask, g, session, request, render_template, redirect, url_for
from flask_cas import CAS, login_required, logout
import urllib.parse
from dotenv import load_dotenv

from discord import OAUTH_URL, VERIFIED_ROLE_ID, SERVER_ID, get_tokens, get_user_info, get_member, add_user_to_server, add_role_to_member, kick_member_from_server, set_member_nickname
import requests

db = redis.from_url(os.environ.get('REDIS_URL'),
                    charset='utf-8', decode_responses=True)

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
        if db.sismember('verified', cas.username):
            return redirect(url_for('joined'))

        user = {}
        if db.get('users:' + cas.username) != None:
            user = json.loads(db.get('users:' + cas.username))

        app.logger.info(f'Home page requested by {cas.username}')
        return render_template('join.html', user=user, rcs_id=cas.username.lower())
    elif request.method == 'POST':
        # Limit to 20 characters so overall Discord nickname doesn't exceed limit of 32 characters
        first_name = request.form['first_name'].strip()[:20]
        last_name = request.form['last_name'].strip()
        graduation_year = request.form['graduation_year'].strip()

        user = {
            'first_name': first_name,
            'last_name': last_name,
            'graduation_year': graduation_year
        }
        db.set('users:' + cas.username, json.dumps(user))

        app.logger.info(f'Redirecting {cas.username} to Discord OAuth page')
        return redirect(OAUTH_URL)


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

    # Get user from DB
    user = json.loads(db.get('users:' + cas.username))

    # Generate nickname as "<first name> <last name initial> '<2 digit graduation year> (<rcs id>)"
    # e.g. "Frank M '22 (matraf)"
    nickname = user['first_name'] + ' ' + \
        user['last_name'][0] + " '" + user['graduation_year'][2:] + \
        f' ({cas.username.lower()})'

    # Exchange authorization code for tokens
    tokens = get_tokens(authorization_code)

    # Get info on the Discord user that just connected (really only need id)
    discord_user = get_user_info(tokens['access_token'])

    # Save to DB
    db.set('discord_user_ids:' + cas.username, discord_user['id'])
    db.set('access_tokens:' + cas.username, tokens['access_token'])

    if not db.sismember('verified', cas.username):
        # Add them to the server
        add_user_to_server(tokens['access_token'],
                           discord_user['id'], nickname)
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

        # Mark success
        db.sadd('verified', cas.username)

    return redirect(url_for('joined'))


@app.route('/discord/reset')
@login_required
def reset_discord():
    discord_user_id = db.get('discord_user_ids:' + cas.username)

    try:
        kick_member_from_server(discord_user_id)
        db.delete('discord_user_ids:' + cas.username)
        db.delete('access_tokens:' + cas.username)
        db.srem('verified', cas.username)
    except:
        raise Exception('Failed to kick your old account from the server.')

    return redirect('/')


@app.route('/joined')
@login_required
def joined():
    if not db.sismember('verified', cas.username):
        return redirect('/')
    user = json.loads(db.get('users:' + cas.username))
    return render_template('joined.html', rcs_id=cas.username.lower(), user=user, discord_server_id=SERVER_ID)


@app.errorhandler(Exception)
def handle_error(e):
    app.logger.exception(e)

    # Hide error in production
    error = e
    if app.env == 'production' and not e.name == 'Not Found':
        error = 'Something went wrong... Please try again later.'

    return render_template('error.html', error=error), 500
