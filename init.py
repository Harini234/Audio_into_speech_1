from flask import Flask
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")

app.config['TEMPLATES_AUTO_RELOAD'] = True

CORS(app)
