from django.shortcuts import render, get_object_or_404
from django.views import View
from django.utils import timezone

from .models import *
from auth_user.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class Requests(View):
    def get(self, request):
        users = User.objects.filter(is_active = False)
        requests = Request.objects.filter(approved=False)

        context = {
            'users' : users,
            'requests_movement' : requests
        }

        return render(request, 'reports/requests.html', context)
    

class ApproveRequestMovement(APIView):
    def get(self, request):
        id = request.query_params.get('id', None)
        
        if id:
            print(f"ID recebido: {id}")
            
            request_movement = get_object_or_404(Request, id=id)

            request_movement.approved = True
            request_movement.dt_response = timezone.now()
            request_movement.save()

            movement = request_movement.fk_movement
            reagent = movement.fk_reagent

            if movement.movement_type == 'A':
                reagent.amount += movement.ammount
            elif movement.movement_type == 'R':
                reagent.amount -= movement.ammount
            
            reagent.save()
            
            return Response({'message': 'Request approved successfully'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'ID não fornecido'}, status=status.HTTP_400_BAD_REQUEST)
