
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def account_verified(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_verified == False:
          flash('Account not verified!')
          return redirect(url_for('auth.inactive'))
        return func(*args, **kwargs)
    return decorated_function