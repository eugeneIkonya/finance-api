from flask import Blueprint, render_template, url_for,flash,redirect

auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.route('/account')
def account():
    return render_template('auth/account.html')