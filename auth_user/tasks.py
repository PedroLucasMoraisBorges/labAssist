from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from core.settings import HOST
from django.urls import reverse

from rest_framework.response import Response
from rest_framework import status
import base64

from auth_user.models import *
import threading

def send_account_activation(user):
    def threadingFunction():
        subject = 'Ativação de conta'
        
        user_id_encoded = base64.b64encode(str(user.id).encode('utf-8')).decode('utf-8')
        link = reverse('user_activation', kwargs={'id': user_id_encoded})

        body = render_to_string(
            'components/emails/account_activation.html',
            {
                'user':user,
                'domain': HOST,
                'link' : link,
            }
        )
        EmailMessage(to = [user.email], subject = subject, body = body).send()

    email_thread = threading.Thread(target=threadingFunction)
    email_thread.start()

        
def send_request_user(user, user_request):
    def threadingFunction():
        subject = 'Requisição de validação de contar de conta'
        body = render_to_string(
            'components/emails/request_user.html',
            {
                'admin':user,
                'user': user_request,
                'domain': HOST
            }
        )
        EmailMessage(to = [user.email], subject = subject, body = body).send()

        email_thread = threading.Thread(target=threadingFunction)
        email_thread.start()