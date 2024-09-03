from app import flask_app,db
from app.models import User

@flask_app.cli.command("create_admin")
def create_admin():
    email = input('Enter Admin Email: ')
    username = input('Enter Admin Username: ')
    first_name = input('Enter Admin First Name: ')
    last_name = input('Enter Admin Last Name: ')
    password = input('Enter Admin Password: ')
    password_confirm = input('Confirm Admin Password: ')

    if password != password_confirm:
        print('Passwords do not match!')
    else:
        try:
            user = User(email=email,
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        password=password,
                        is_admin=True,
                        is_verified=True)
            db.session.add(user)
            db.session.commit()
            print('Admin Created!')
        except Exception as e:
            print(e)
            print('Error creating admin!')