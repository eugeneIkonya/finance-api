from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import DevelopmentConfig
from flask_mail import Mail
from flask_smorest import Api
from flask_cors import CORS


flask_app = Flask(__name__)

flask_app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(flask_app)
mail  = Mail(flask_app)

Migrate(flask_app,db)


api = Api(flask_app)
cors = CORS(flask_app, resources={r"/*" : {"origins" : "*"} })

@flask_app.route('/')
def index():
    return render_template('index.html')

from app.auth.api import auth
api.register_blueprint(auth)

from app.utils.comands import create_admin