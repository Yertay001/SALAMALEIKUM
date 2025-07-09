from django.core.mail import send_mail
from django.conf import settings

def send_msg(user_email):
    subject = 'Welcome to Our Service'
    message = 'Thank you for registering with us!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
    print(f"Email sent to {user_email} successfully.")

def send_auth_code(email, auth_code):
    subject = 'Your Authentication Code'
    message = f'Your authentication code is: {auth_code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    print(f"Authentication code sent to {email} successfully.")