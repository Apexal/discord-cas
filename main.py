import os
from utils import hget_json
import redis
import json
from flask import Flask, g, session, request, render_template, redirect, url_for, abort
from flask_cas import CAS, login_required, logout
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException
import yaml

from discord import BOT_JOIN_URL, OAUTH_URL, get_member, get_tokens, get_user, get_user_info, add_user_to_server, add_role_to_member, kick_member_from_server, set_member_nickname
import requests

# Connect to Redis
db = redis.from_url(os.environ.get('REDIS_URL'),
                    charset='utf-8', decode_responses=True)

# Load .env into os.environ
load_dotenv()

with open('clients.yml') as f:
    clients = yaml.load(f, Loader=yaml.FullLoader)

app = Flask(__name__)
cas = CAS(app, '/cas')

app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.config['CAS_SERVER'] = 'https://cas-auth.rpi.edu/cas/login'
app.config['CAS_AFTER_LOGIN'] = 'index'


@app.before_request
def before_request():
    '''Runs before every request.'''

    # Everything added to g can be accessed during the request
    g.is_logged_in = cas.username is not None
    g.username = cas.username.lower() if g.is_logged_in else None
    g.client_id = session['client_id'] if 'client_id' in session else None
    g.client = clients[g.client_id] if g.client_id is not None else None


@app.context_processor
def add_template_locals():
    '''Add values to be available to every rendered template.'''

    # Add keys here
    return {
        'is_logged_in': g.is_logged_in,
        'username': g.username,
        'client_id': g.client_id,
        'client': g.client
    }


@app.route('/test')
def test():
    return 'Testing'


@app.route('/test_redis')
def test_redis():
    val = db.get('test')
    return 'Testing redis: ' + val

@app.route('/')
def splash():
    return render_template('splash.html', bot_join_url=BOT_JOIN_URL)

@app.route('/bot_invite')
def bot_invite():
    return redirect(BOT_JOIN_URL)

@app.route('/<string:client_id>', methods=['GET'])
@login_required
def index(client_id):
    if client_id not in clients:
        abort(404, 'Unknown Client')

    # Set client
    client = clients[client_id]
    g.client_id = client_id
    g.client = client
    session['client_id'] = client_id

    # Determine status of user
    # Users can:
    # 1) Not have connected to Discord
    # 2) Not have filled their profile
    # 3) Both 1 and 2
    # 4) Joined the server (after 1 and 2)

    # Only exists if user has set profile
    profile = hget_json(db, 'profiles', g.username)

    # Only exists if user has connected Discord account
    discord_account_id = db.hget('discord_account_ids', g.username)
    discord_user = get_user(discord_account_id) if discord_account_id else None

    # Only exists if user has joined server
    discord_member = get_member(
        client['discord']['server_id'], discord_account_id) if discord_user else None

    return render_template('index.html', profile=profile, discord_user=discord_user, discord_member=discord_member, discord_oauth_url=OAUTH_URL, rcs_id=g.username)


@app.route('/profile', methods=['POST'])
def profile():
    if request.method == 'POST':
        # Grab from form and set profile
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        graduation_year = request.form['graduation_year'].strip()
        # timezone = request.form['timezone']

        profile = {
            'first_name': first_name,
            'last_name': last_name,
            'graduation_year': graduation_year,
            # 'timezone': timezone
        }
        db.hset('profiles', g.username, json.dumps(profile))

        # If user has joined Discord server, change their nickname
        # Only exists if user has connected Discord account
        discord_account_id = db.hget('discord_account_ids', g.username)
        discord_user = get_user(
            discord_account_id) if discord_account_id else None

        # Only exists if user has joined server
        discord_member = get_member(
            g.client['discord']['server_id'], discord_account_id) if discord_user else None

        if discord_member:
            # Generate nickname as "<first name> <last name initial> '<2 digit graduation year> (<rcs id>)"
            # e.g. "Frank M '22 (matraf)"
            new_nickname = profile['first_name'][:20] + ' ' + \
                profile['last_name'][0] + " '" + profile['graduation_year'][2:] + \
                f' ({g.username})'

            server_id = g.client['discord']['server_id']

            # Set their nickname
            try:
                set_member_nickname(server_id, discord_account_id, new_nickname)
                app.logger.info(
                    f'Updated {g.username}\'s nickname to "{new_nickname}" on server')
            except requests.exceptions.HTTPError as e:
                app.logger.warning(
                    f'Failed to UPDATE nickname "{new_nickname}" to {g.username} on {g.client_id} server: {e}')

        return redirect(url_for('index', client_id=g.client_id))


@app.route('/profile/reset')
@login_required
def reset_profile():
    # Attempt to kick member from server and then remove DB records
    db.hdel('profiles', g.username)

    return redirect(url_for('index', client_id=g.client_id))


@app.route('/join')
def join():
    server_id = g.client['discord']['server_id']
    verified_role_ids = g.client['discord']['verified_role_ids']

    # Get profile
    profile = hget_json(db, 'profiles', g.username)

    # Generate nickname as "<first name> <last name initial> '<2 digit graduation year> (<rcs id>)"
    # e.g. "Frank M '22 (matraf)"
    nickname = profile['first_name'][:20] + ' ' + \
        profile['last_name'][0] + " '" + profile['graduation_year'][2:] + \
        f' ({g.username})'

    discord_user_id = db.hget('discord_account_ids', g.username)
    tokens = hget_json(db, 'discord_account_tokens', g.username)

    print('discord_user_id', discord_user_id)
    print('tokens', tokens)
    print('access_token', tokens['access_token'])

    # Add them to the server
    add_user_to_server(server_id, tokens['access_token'],
                       discord_user_id, nickname, verified_role_ids)
    app.logger.info(f'Added {g.username} to {g.client["title"]} server')

    # Set their nickname
    try:
        set_member_nickname(server_id, discord_user_id, nickname)
        app.logger.info(
            f'Set {g.username}\'s nickname to "{nickname}" on server')
    except requests.exceptions.HTTPError as e:
        app.logger.warning(
            f'Failed to set nickname "{nickname}" to {g.username} on {g.client_id} server: {e}')

    # Give them the verified roles
    for role_id in verified_role_ids:
        try:
            add_role_to_member(server_id, discord_user_id, role_id)
            app.logger.info(f'Added verified role to {g.username} on server')
        except requests.exceptions.HTTPError as e:
            app.logger.warning(
                f'Failed to add role to {g.username} on server: {e}')

    return redirect(url_for('index', client_id=g.client_id))


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
                f'{g.username} declined to connect their Discord account')
            return render_template('error.html', error='You declined to connect your Discord account!')
        else:
            # Handle generic Discord error
            error_description = request.args.get('error_description')
            app.logger.error(
                f'An error occurred on the Discord callback for {g.username}: {error_description}')
            raise Exception(error_description)

    # Exchange authorization code for tokens
    tokens = get_tokens(authorization_code)
    print('tokens', tokens)

    # Get info on the Discord user that just connected (really only need id)
    discord_user = get_user_info(tokens['access_token'])
    print('discord_user', discord_user)

    # Save to DB
    db.hset('discord_account_ids', g.username, discord_user['id'])
    db.hset('discord_account_tokens', g.username, json.dumps(tokens))

    return redirect(url_for('index', client_id=g.client_id))


@app.route('/discord/reset')
@login_required
def reset_discord():
    discord_user_id = db.hget('discord_account_ids', g.username)
    server_id = g.client['discord']['server_id']

    print('discord_user_id', discord_user_id)

    # Attempt to kick member from server and then remove DB records
    db.hdel('discord_account_ids', g.username)
    db.hdel('discord_account_tokens', g.username)
    print('discord_user_id', discord_user_id)
    try:
        kick_member_from_server(server_id, discord_user_id)
    except:
        raise Exception('Failed to kick your old account from the server.')

    return redirect(url_for('index', client_id=g.client_id))


@app.errorhandler(404)
def page_not_found(e):
    '''Render 404 page.'''
    return render_template('404.html'), 404


@app.errorhandler(Exception)
def handle_exception(e):
    '''Handles all unhandled exceptions.'''

    # Handle HTTP errors
    if isinstance(e, HTTPException):
        return render_template('error.html', error=e), e.code

    # Handle non-HTTP errors
    app.logger.exception(e)

    # Hide error details in production
    if app.env == 'production':
        e = 'Something went wrong... Please try again later.'

    return render_template('error.html', error=e), 500
