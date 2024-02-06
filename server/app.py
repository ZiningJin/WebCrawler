from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from api.routes import api
from config import Config
from models import db
import logging

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(api, url_prefix='/api')

logging.basicConfig(level=logging.INFO)

@app.route('/')
def hello_charlie():
    return "Hello, Charlie!"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

if __name__ == '__main__':
    app.run(debug=True)
