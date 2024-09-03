from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import DevelopmentConfig
from flask_mail import Mail


flask_app = Flask(__name__)

flask_app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(flask_app)
mail  = Mail(flask_app)

Migrate(flask_app,db)

login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = 'auth.login'




from app.core.views import core
flask_app.register_blueprint(core)

from app.error_pages.handlers import error_pages
flask_app.register_blueprint(error_pages)

from app.auth.views import auth
flask_app.register_blueprint(auth)

from app.utils.comands import create_admin