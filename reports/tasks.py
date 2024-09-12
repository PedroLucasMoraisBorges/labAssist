from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from core.settings import HOST

# tasks.py

def send_activation_email(user):
    subject = 'Conta ativada'
    body = render_to_string(
        'components/emails/confirmation.html',
        {
            'user': user,
            'domain': HOST
        }
    )
    EmailMessage(to = [user.email], subject = subject, body = body).send()