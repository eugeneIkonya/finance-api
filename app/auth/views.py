from datetime import datetime
from flask import Blueprint,render_template, url_for,flash,redirect,request
from flask_login import login_user,login_required,logout_user,current_user
from app import db, flask_app
from app.models import User
from app.auth.forms import LoginForm, SignupForm, UpdateUserForm, ChangePasswordForm, ForgotPasswordForm, ResetPasswordForm
from app.auth.picture_handler import add_profile_pic
from app.auth.tokens import generate_confirmation_token, confirm_token
from app.utils.mail import send_email
from app.utils.decorators import account_verified


auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged In!')

            next = request.args.get('next')

            if next is None or not isinstance(next, str) or not next.startswith('/'):
                next = url_for('core.index')

            return redirect(next)

    return render_template('auth/login.html', form=form)

@auth.route('/signup',methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data)
        
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('auth/confirm_email.html', confirm_url=confirm_url)
        subject = "EugeneIkonya Website - Account Verification"
        recipients = [user.email]
        send_email(subject, recipients, html)
        
        login_user(user)

        flash('A confirmation Email has been sent via email!')
        return redirect(url_for('auth.inactive'))
    
    return render_template('auth/signup.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.is_verified:
        flash('Account already verified!')
        return redirect(url_for('core.index'))
    email = confirm_token(token)
    user = db.session.query(User).filter_by(email=email).first()
    if user.email == email:
        user.is_verified = True
        user.updated_at = datetime.now()
        db.session.commit()
        flash('Account verified!')
    else:
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for('core.index'))

@auth.route('/inactive')
@login_required
def inactive():
    if current_user.is_verified:
        return redirect(url_for('core.index'))
    return render_template('auth/inactive.html')

@auth.route('/resend')
@login_required
def resend_confirmation():
    if current_user.is_verified:
        flash('Account already verified!')
        return redirect(url_for('core.index'))
    
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/confirm_email.html', confirm_url=confirm_url)
    subject = "EugeneIkonya Website - Account Verification"
    recipients = [current_user.email]
    send_email(subject, recipients, html)




@auth.route('/account',methods=['GET','POST'])
@login_required
@account_verified
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.profile_picture.data:
            username = current_user.username
            profile_picture = add_profile_pic(form.profile_picture.data, username)
            if profile_picture:
                current_user.profile_picture = profile_picture
            else:
                flash('Profile Picture upload failed!')
            
            current_user.profile_picture = profile_picture
        
        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.updated_at = datetime.now()

        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('auth.account'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name

    return render_template('auth/account.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@auth.route('/change_password',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = current_user
        user.update_password(form.new_password.data)
        flash('Password Updated!')
        return redirect(url_for('auth.account'))
      

    return render_template('auth/change_password.html',form=form)

@auth.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.reset_password', token=token, _external=True)
        html = render_template('auth/reset_password_email.html', confirm_url=confirm_url)
        subject = "EugeneIkonya Website - Reset Password"
        recipients = [user.email]
        send_email(subject, recipients, html)
        flash('A password reset link has been sent via email!')
        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html',form=form)

@auth.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    email = confirm_token(token)
    user = db.session.query(User).filter_by(email=email).first()

    if user.email == email:
        form = ResetPasswordForm()
     
        if form.validate_on_submit():
            user.update_password(form.new_password.data)
            db.session.commit()
            flash('Password Updated!')
            return redirect(url_for('auth.login'))
        return render_template('auth/reset_password.html',form=form)
    else:
        flash("The reset link is invalid or has expired.")
        return redirect(url_for('auth.login'))