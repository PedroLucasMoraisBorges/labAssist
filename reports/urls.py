from django.urls import path
from .views import *

urlpatterns = [
    path('requisções/', Requests.as_view(), name='requests'),
    path('aprovarMovimentação/', ApproveRequestMovement.as_view(), name='approve_request_movement'),
    path('desaprovarMovimentação/', DesapproveRequestMovement.as_view(), name='desapprove_request_movement'),
    path('ativarUsuario/',ApproveUser.as_view(), name='approve_user'),
    path('desaprovarUsuario/', DisapproveUser.as_view(), name='desapprove_user'),
]