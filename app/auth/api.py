from pyexpat.errors import messages

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app import db
from app.auth.schema import UserSchema, CreateUserSchema, LoginUserSchema, UpdatePasswordSchema, UpdateUsernameSchema, \
    UpdateEmailSchema
from app.auth.tokens import generate_confirmation_token
from app.models import User

auth = Blueprint("User","user",url_prefix='/user', description="User endpoints")

@auth.route('/')
class Users(MethodView):
    @auth.response(200, UserSchema(many=True))
    def get(self):
        users = db.session.query(User).all()
        return users

    @auth.arguments(CreateUserSchema)
    @auth.response(200)
    def post(self, data):
        user = User(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )
        if db.session.query(User).filter_by(username = user.username).first():
            abort(400, message="Username Exists")
        if db.session.query(User).filter_by(email = user.email).first():
            abort(401, message="Email exists")
        db.session.add(user)
        db.session.commit()

        return "Account Created"

@auth.route('/<user_id>')
class UserByID(MethodView):
    @auth.response(200, UserSchema)
    def get(self, user_id):
        user = db.session.query(User).get(user_id)
        if not user:
            abort(404, message = "User not Found")
        return user


    @auth.arguments(CreateUserSchema)
    @auth.response(200)
    def put(self, data, user_id):
        user = db.session.query(User).get(user_id)
        if not user:
            abort(404, message="User not Found")

        user.email = data["email"]
        user.username = data["username"]
        user.password = data["password"]

        db.session.commit()
        return "User Updated"

    @auth.response(200)
    def delete(self,user_id):
        user = db.session.query(User).get(user_id)
        if not user:
            abort(404, message="User not Found")

        db.session.delete(user)
        db.session.commit()
        return "User Deleted"

@auth.route('/login')
class Login(MethodView):
    @auth.arguments(LoginUserSchema)
    @auth.response(200, UserSchema)
    def post(self, data):
        email = data["email"]
        password = data["password"]

        user = db.session.query(User).filter_by(email=email).first()

        if not user:
            abort(404, message="User not Found")
        if not user.check_password(password):
            abort(401, messages="Incorrect Password")

        return user


@auth.route('/verify-user/<user_id>')
class VerifyUser(MethodView):
    @auth.response(200)
    def post(self,user_id):
        user = db.session.query(User).get(user_id)
        if not user:
            abort(404, message="User not Found")

        user.is_verified = True
        db.session.commit()
        return "User Verified"

@auth.route('/reset-password/<user_id>')
class ResetPassword(MethodView):
    @auth.arguments(UpdatePasswordSchema)
    @auth.response(200)
    def patch(self, data, user_id):
        user = db.session.query(User).get(user_id)
        if not user:
            abort(404, message="User not Found")
        user.update_password(data['password'])
        db.session.commit()

@auth.route('update_username/<user_id>')
class UpdateUsername(MethodView):
    @auth.arguments(UpdateUsernameSchema)
    @auth.response(200)
    def patch(self, data, user_id):
        user = db.session.query(User).get(user_id)
        if not user:
            abort(404, message="User not Found")
        user.username = data['username']
        db.session.commit()
        return 'Username Updated'

@auth.route('update_email/<user_id>')
class UpdateEmail(MethodView):
    @auth.arguments(UpdateEmailSchema)
    @auth.response(200)
    def patch(self, data, user_id):
        user = db.session.query(User).get(user_id)
        if not user:
            abort(404, message="User not Found")

        user.email = data['email']
        user.is_verified = False
        db.session.commit()

        return "Email Updated"