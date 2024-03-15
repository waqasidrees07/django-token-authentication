from django.core.mail import EmailMessage
from rest_framework.response import Response
import os

def send_my_email(email, subject, body):
    mail = EmailMessage(
        str(subject),
        str(body),
        os.environ.get("EMAIL_HOST_USER"),
        [email],
    )
    mail.send()
    return True
