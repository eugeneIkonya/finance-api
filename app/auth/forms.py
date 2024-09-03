from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from app.models import User 
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from app import db

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(),Length(5,64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_email(self, field):
        if not db.session.query(User).filter_by(email=field.data).first():
            raise ValidationError('Incorrect Email!')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(),Length(5,64)])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired(),Length(3,64)])
    last_name = StringField('Last Name', validators=[DataRequired(),Length(3,64)])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('password_confirm',message='Passwords must match')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')
    
    def validate_username(self, field):
        if db.session.query(User).filter_by(username=field.data).first():
            raise ValidationError('Your username has been registered already!')
        
    
class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired(),Length(3,64)])
    last_name = StringField('Last Name', validators=[DataRequired(),Length(3,64)])
    profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).first() and field.data != current_user.email:
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        if db.session.query(User).filter_by(username=field.data).first() and field.data != current_user.username:
            raise ValidationError('Your username has been registered already!')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(),EqualTo('new_password_confirm',message='Passwords must match')])
    new_password_confirm = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Update Password')
    
    def validate_old_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError('Your old password is incorrect!')
        
    def validate_new_password(self, field):
        if current_user.check_password(field.data):
            raise ValidationError('Your new password must be different from your old password!')
            
class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(),EqualTo('new_password_confirm',message='Passwords must match')])
    new_password_confirm = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Update Password')
    
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')
    
    def validate_email(self, field):
        if not db.session.query(User).filter_by(email=field.data).first():
            raise ValidationError('Your email is not registered!')