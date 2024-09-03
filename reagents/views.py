from django.shortcuts import render
from django.views import View

from .models import *
from reports.models import *
from django.db.models import Q

# Create your views here.

class LandingPage(View):
    def get(self, request):
        return render(request, 'landingPage.html')

class HomeAdmin(View):
    def get(self, request):
        geralVision = Reagent.objects.filter(~Q(formula=''))
        recentMovement = Movement.objects.filter().order_by('dt_movement')
        inventoryBalance = Reagent.objects.filter().order_by('amount')