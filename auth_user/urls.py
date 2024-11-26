from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('cadastro/', RegisterUser.as_view(), name='register'),
    path('usuárioInativo/', AlertUserInactive.as_view(), name='alert_user_inactive'),
    path('ativarUsuario/<str:id>',UserActivate.as_view(), name='user_activation'),
    path('usuarios/', Users.as_view(), name='users'),
    path('paginaUsuario/<str:id>', ViewUserProfile.as_view(), name='user_page'),
    path('', Redirect.as_view(), name=''),
    path('perfil/', ViewUserProfile.as_view(), name='user_profile'),
    path('perfil/editar/', EditProfile.as_view(), name='edit_profile'),
    path('gerenciarUsuario/<str:id>', ManageUser.as_view(), name='manage_user')
]