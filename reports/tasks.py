from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from core.settings import HOST

from rest_framework.response import Response
from rest_framework import status

import threading

# tasks.py

def send_activation_email(user):
    def threadingFunction():
        subject = 'Conta ativada'
        body = render_to_string(
            'components/emails/confirmation.html',
            {
                'user': user,
                'domain': HOST
            }
        )
        EmailMessage(to = [user.email], subject = subject, body = body).send()

    email_thread = threading.Thread(target=threadingFunction)
    email_thread.start()

    return Response({'message' : 'User ativado com sucesso'}, status=status.HTTP_200_OK)

def send_cancellation_email(user):
    def threadingFunction():
        subject = 'Conta deletada'
        body = render_to_string(
            'components/emails/cancellation.html',
            {
                'user': user,
                'domain': HOST
            }
        )
        EmailMessage(to = [user.email], subject = subject, body = body).send()

    email_thread = threading.Thread(target=threadingFunction)
    email_thread.start()
    user.delete()

    return Response({'message' : 'User ativado com sucesso'}, status=status.HTTP_200_OK)

def send_request_user(user, user_request):
    def threadingFunction():
        subject = 'Requisição de ativação de conta'
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

def send_request_movement(user, request):
    def threadingFunction():
        subject = 'Requisição de ativação de conta'
        body = render_to_string(
            'components/emails/request_movement.html',
            {
                'admin':user,
                'movement': request,
                'domain': HOST
            }
        )
        EmailMessage(to = [user.email], subject = subject, body = body).send()

        email_thread = threading.Thread(target=threadingFunction)
        email_thread.start()