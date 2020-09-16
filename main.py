import os
from flask import Flask, g, session, request, render_template, redirect, url_for
from flask_cas import CAS, login_required, logout
from dotenv import load_dotenv

from discord import DISCORD_BOT_TOKEN

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
    return 'Hello, ' + cas.username
