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

    API_TITLE = "c5 Finance API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = "/api-doc"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DEBUG_TB_ENABLED = True

class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False