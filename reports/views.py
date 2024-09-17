from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.utils import timezone
import base64
import threading
from .tasks import *

from .models import *
from auth_user.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from core.settings import HOST

class Requests(View):
    def get(self, request):
        users = User.objects.filter(is_active = False)
        requests = Request.objects.filter(approved=False, dt_response=None)
        inactiveUsers = []
        listRequests = []


        
        for user in users:
            user_id_encoded = base64.b64encode(str(user.id).encode('utf-8')).decode('utf-8')
            inactiveUsers.append(
                {
                    'codifiqued_id' : user_id_encoded,
                    'info' : user,
                    'urls' : {
                        'approve' : HOST + reverse('approve_user'),
                        'desapprove' : HOST + reverse('desapprove_user')
                    }
                }
            )
        
        for item in requests:
            listRequests.append(
                {
                    'info' : item,
                    'urls' : {
                        'approve' : HOST + reverse('approve_request_movement'),
                        'desapprove' : HOST + reverse('desapprove_request_movement')
                    }
                }
            )

        context = {
            'users' : inactiveUsers,
            'requests_movement' : listRequests
        }

        return render(request, 'reports/requests.html', context)
    

# MOVEMENT


class ApproveRequestMovement(APIView):
    def get(self, request):
        id = request.query_params.get('id', None)
        
        if id:            
            request_movement = get_object_or_404(Request, id=id)

            request_movement.approved = True
            request_movement.dt_response = timezone.now()
            request_movement.save()

            movement = request_movement.fk_movement
            reagent = movement.fk_reagent

            if movement.movement_type == 'A':
                reagent.amount += movement.ammount
            elif movement.movement_type in ['R', 'T']:
                reagent.amount -= movement.ammount
            
            reagent.save()
            
            return Response({'message': 'Requisição aprovada com sucesso'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'ID não fornecido'}, status=status.HTTP_400_BAD_REQUEST)
    
class DesapproveRequestMovement(APIView):
    def get(self, request):
        id = request.query_params.get('id', None)
        
        if id:            
            request_movement = get_object_or_404(Request, id=id)
            request_movement.dt_response = timezone.now()
            request_movement.save()
            
            return Response({'message': 'Requisição aprovada com sucesso'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'ID não fornecido'}, status=status.HTTP_400_BAD_REQUEST)
    

# USER


class ApproveUser(APIView):
    def get(self, request):
        codifiquedId = request.query_params.get('id', None)

        if codifiquedId:
            decoded_id = base64.b64decode(codifiquedId).decode('utf-8')

            user = User.objects.get(id=decoded_id)

            if user:
                user.save()
                return send_activation_email(user)  
                      
            return Response({'error': 'User não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'error': 'ID não fornecido'}, status=status.HTTP_400_BAD_REQUEST)

class DisapproveUser(APIView):
    def get(self, request):
        codifiquedId = request.query_params.get('id', None)

        if codifiquedId:
            decoded_id = base64.b64decode(codifiquedId).decode('utf-8')
            user = User.objects.get(id=decoded_id)

            if user:
                return send_cancellation_email(user)
                      
            return Response({'error': 'User não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'error': 'ID não fornecido'}, status=status.HTTP_400_BAD_REQUEST)