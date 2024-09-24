from django.shortcuts import render, redirect
from django.views import View

from .models import *
from .forms import *
from reports.models import *
from django.db.models import Q
from GeralUtilits import getErrors
from .utilits import *

# Create your views here.

class LandingPage(View):
    def get(self, request):
        return render(request, 'landingPage.html')

class HomeAdmin(View):
    def get(self, request):            
        liquids = Reagent.objects.filter(state='L')
        solids = Reagent.objects.filter(state='S')

        recentMovement = Movement.objects.filter().order_by('dt_movement')
        inventoryBalance = Reagent.objects.filter().order_by('amount')

        context = {
            'solids' : agrupar_reagents_por_letra(ordenar_lista(solids)),
            'liquids' : agrupar_reagents_por_letra(ordenar_lista(liquids)),
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

class ViewLiquids(View):
    def get(self, request):
        search = request.GET.get('search', "")

        passive_liquids = search_for_reagent(search, 'L')['passives']
        active_liquids = search_for_reagent(search, 'L')['actives']

        context = {
            'active_liquids' : agrupar_reagents_por_letra(ordenar_lista(active_liquids)),
            'passive_liquids' : agrupar_reagents_por_letra(ordenar_lista(passive_liquids))
        }
        return render(request, 'reagents/liquids.html', context)
    
class ViewSolids(View):
    def get(self, request):
        search = request.GET.get('search', "")

        passive_solids = search_for_reagent(search, 'S')['passives']
        active_solids = search_for_reagent(search, 'S')['actives']

        context = {
            'active_liquids' : agrupar_reagents_por_letra(ordenar_lista(active_solids)),
            'passive_liquids' : agrupar_reagents_por_letra(ordenar_lista(passive_solids))
        }
        return render(request, 'reagents/liquids.html', context)