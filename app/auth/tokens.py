from app import flask_app
from itsdangerous import URLSafeTimedSerializer

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(flask_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=flask_app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(flask_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=flask_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
        return email
    except:
        return False
    