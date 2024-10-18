from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('cadastro/', RegisterUser.as_view(), name='register'),
    path('usuarios/', Users.as_view(), name='users'),
    path('paginaUsuario/<str:id>', UserPage.as_view(), name='user_page'),
    path('', Redirect.as_view(), name=''),
]