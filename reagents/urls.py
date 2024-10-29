from django.urls import path
from .views import *

urlpatterns = [
    path('landingPage', LandingPage.as_view(), name='landing_page'),
    path('home/', HomeAdmin.as_view(), name='home_admin'),
    path('cadastrarReagente/', RegisterReagent.as_view(), name='register_reagent'),
    path('editarReagente/<str:id>', EditReagent.as_view(), name='edit_reagent'),
    path('estoque/liquidos/', ViewLiquids.as_view(), name='stock_liquids'),
    path('estoque/sólidos/', ViewSolids.as_view(), name='stock_solids'),
]