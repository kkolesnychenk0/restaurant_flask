import yagmail
from flask import render_template


def send_email(subject, recipients, text_body):
    try:
        # initializing the server connection
        yag = yagmail.SMTP(user='trachmail0@gmail.com', password='kixxldawolqlgbae')
        yag.send(recipients, subject, text_body)
        print("Email sent successfully")
    except:
        print("Error, email was not sent")


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Fridays] Reset Your Password', user.email,
               render_template('email/reset_password.txt', user=user, token=token))
