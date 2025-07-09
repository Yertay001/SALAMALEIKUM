from celery import shared_task
from .utils import send_msg, send_auth_code

@shared_task
def send_welcome_message_async(email):
    send_msg(email)

@shared_task
def send_auth_code_async(email, auth_code):
    send_auth_code(email, auth_code)

