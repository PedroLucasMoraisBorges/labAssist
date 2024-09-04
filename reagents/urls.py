from django.urls import path
from .views import *

urlpatterns = [
    path('landingPage', LandingPage.as_view(), name='landing_page'),
    path('cadastrarReagente/', RegisterReagent.as_view(), name='register_reagent'),
]