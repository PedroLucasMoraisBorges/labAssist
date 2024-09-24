from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('cadastro/', RegisterUser.as_view(), name='register'),
    path('usuarios/', Users.as_view(), name='users'),
    path('', Redirect.as_view(), name=''),
]