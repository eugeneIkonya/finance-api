from app import flask_app, mail
from flask_mail import Message

def send_email(subject, recipients, template):
    message = Message(
        subject,
        recipients=recipients,
        html=template,
        sender=flask_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(message)
