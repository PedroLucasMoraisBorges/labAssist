from django.urls import path
from .views import *

urlpatterns = [
    path('pendências/', Pendings.as_view(), name='pendings'),
    path('aprovarMovimentação/', ApproveRequestMovement.as_view(), name='approve_request_movement'),
    path('desaprovarMovimentação/', DesapproveRequestMovement.as_view(), name='desapprove_request_movement'),
    path('ativarUsuario/',ApproveUser.as_view(), name='approve_user'),
    path('desaprovarUsuario/', DisapproveUser.as_view(), name='desapprove_user'),
    path('createMovement/', CrateMovement.as_view(), name='create_movement'),
    path('movimentações/', Movements.as_view(), name='movements'),
    path('cadastroLisença/', RegisterLicense.as_view(), name='register_license'),
]