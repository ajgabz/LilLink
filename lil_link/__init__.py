import os
import redis
from flask import Flask
from flask_reggie import Reggie

app = Flask(__name__)
app.config.from_object('config')

Reggie(app)

# If this app is running under Heroku, then we reconfigure the config variables
if os.environ.get('HEROKU') is not None:
    app.config["DEBUG"] = False
    app.config["SECRET_KEY"] = os.environ.get("DEPLOYED_SECRET_KEY")
    app.config["LILLINK_REDIS_URL"] = os.environ.get("REDIS_URL")

# Set the secret key, which is necessary for flashing
app.secret_key = app.config["SECRET_KEY"]

r = redis.from_url(app.config["LILLINK_REDIS_URL"])

# If the global 'siteCounter' key is not set, then we initialize it now.
r.setnx('siteCounter', 0)

import lil_link.shortener
import lil_link.errors