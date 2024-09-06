from django.urls import path
from .views import *

urlpatterns = [
    path('landingPage', LandingPage.as_view(), name='landing_page'),
    path('home/', HomeAdmin.as_view(), name='home_admin'),
    path('cadastrarReagente/', RegisterReagent.as_view(), name='register_reagent'),
]