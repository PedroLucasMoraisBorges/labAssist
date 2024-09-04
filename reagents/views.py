from django.shortcuts import render, redirect
from django.views import View

from .models import *
from .forms import *
from reports.models import *
from django.db.models import Q
from GeralUtilits import getErrors

# Create your views here.

class LandingPage(View):
    def get(self, request):
        return render(request, 'landingPage.html')

class HomeAdmin(View):
    def get(self, request):
        geralVision = Reagent.objects.filter(~Q(formula=''))
        recentMovement = Movement.objects.filter().order_by('dt_movement')
        inventoryBalance = Reagent.objects.filter().order_by('amount')

        context = {
            'geralVision' : geralVision,
            'recentMovement' : recentMovement,
            'inventoryBalance' : inventoryBalance
        }
        
        return render(request, 'admin/homeAdmin.html', context)

class RegisterReagent(View):
    def get(self, request):
        reagentForm = ReagentForm()

        context = {
            'form' : reagentForm
        }

        return render(request, 'reagents/register.html', context)
    
    def post(self, request):
        reagentForm = ReagentForm(request.POST)

        errors = getErrors([reagentForm])

        if reagentForm.is_valid():
            reagentForm.save()
            return redirect('/')
        else:
            context = {
                'form' : reagentForm,
                'errors' : errors
            }

            return render(request, 'reagents/register.html', context)

