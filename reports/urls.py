from django.urls import path
from .views import *

urlpatterns = [
    path('pendências/', Pendings.as_view(), name='pendings'),
    # API
    path('aprovarMovimentação/', ApproveRequestMovement.as_view(), name='approve_request_movement'),
    path('desaprovarMovimentação/', DesapproveRequestMovement.as_view(), name='desapprove_request_movement'),
    path('ativarUsuario/',ApproveUser.as_view(), name='approve_user'),
    path('desaprovarUsuario/', DisapproveUser.as_view(), name='desapprove_user'),
    path('createMovement/', CreateMovement.as_view(), name='create_movement'),

    # ROTA NORMAL
    path('movimentações/', Movements.as_view(), name='movements'),
    path('cadastroLisença/', RegisterLicense.as_view(), name='register_license'),
]