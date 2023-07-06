from flask import Flask
from flask_caching import Cache
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_envvar('APPLICATION_SETTINGS')

CORS(app)

cache = Cache(app)