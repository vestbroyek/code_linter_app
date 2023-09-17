from authlib.integrations.flask_client import OAuth
from datetime import datetime
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

# Connect to the database
# run with: docker run -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=linter --rm postgres
load_dotenv(find_dotenv())
database_uri = env.get("SQLALCHEMY_DATABASE_URI")

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI=database_uri,
    FLASK_ENV="development",
    DEBUG=True,
    SECRET_KEY=env.get("APP_SECRET_KEY"),
)
db.init_app(app)

CORS(app)

# Auth0 set up
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "mcb.westbroek@gmail.com",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Misc - date format
def format_date(value):
    date_created = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
    return date_created.strftime("%A, %d %B %Y")


# Add the custom filter to Jinja2 environment
app.jinja_env.filters["format_date"] = format_date

# Auth0 Config
AUTH0_DOMAIN = "dev-alz530yb27kb08mr.us.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "linter"
