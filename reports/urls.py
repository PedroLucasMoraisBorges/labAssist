from django.urls import path
from .views import *

urlpatterns = [
    path('requisções/', Requests.as_view(), name='requests'),
    path('aprovar-requisicao/', ApproveRequestMovement.as_view(), name='approve_request_movement'),
    path('ativarUsuario/',ApproveUser.as_view(), name='approve_user'),
]