import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object): 
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "your_secret_key_here"
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir,"data.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'eugeneikonyawebsite@gmail.com'
    MAIL_PASSWORD = 'doykbnwmlptidfyn'
    MAIL_DEFAULT_SENDER = 'eugeneikonyawebsite@gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    SECURITY_PASSWORD_SALT = 'my_precious_two'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DEBUG_TB_ENABLED = True

class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False