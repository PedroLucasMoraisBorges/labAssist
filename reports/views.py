from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.utils import timezone
import base64
from .tasks import *
from .forms import *
from .models import *
from auth_user.models import *
from reagents.utilits import *

from reagents.models import *
from reagents.utilits import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from core.settings import HOST
from GeralUtilits import *

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from auth_user.decorators import *


class Pendings(View):
    @method_decorator(login_required)
    @method_decorator(superuser_required)
    def get(self, request):
        users = User.objects.filter(is_active=False, approved=True)
        requests = Request.objects.filter(approved=False, dt_response=None)
        license = License.objects.filter(is_expired=False).first()
        inactiveUsers = []
        listRequests = []

        for user in users:
            user_id_encoded = base64.b64encode(str(user.id).encode("utf-8")).decode(
                "utf-8"
            )
            inactiveUsers.append(
                {
                    "codifiqued_id": user_id_encoded,
                    "info": user,
                    "urls": {
                        "approve": HOST + reverse("approve_user"),
                        "desapprove": HOST + reverse("desapprove_user"),
                    },
                }
            )

        for item in requests:
            listRequests.append(
                {
                    "info": item,
                    "urls": {
                        "approve": HOST + reverse("approve_request_movement"),
                        "desapprove": HOST + reverse("desapprove_request_movement"),
                    },
                }
            )

        balance_maturity = ReagentBatch.objects.filter(amount__gt=0).order_by("amount")[:5]

        context = {
            "users": inactiveUsers,
            "requests_movement": listRequests,
            "balance_maturity": balance_maturity,
            "license" : license
        }

        return render(request, "reports/requests.html", context)


# MOVEMENT


class Movements(View):
    @method_decorator(login_required)
    @method_decorator(superuser_required)
    def get(self, request):
        movements = Movement.objects.all()

        add_movements = []
        removed_movements = []

        for movement in movements:
            req = Request.objects.get(fk_movement=movement)
            if req.approved == True and req.dt_response != None:
                if movement.movement_type in ["R", "T"]:
                    removed_movements.append(movement)
                else:
                    add_movements.append(movement)

        context = {
            "added_movements": add_movements,
            "removed_movements": removed_movements,
        }

        return render(request, "reports/movements.html", context)


class CreateMovement(APIView):
    @method_decorator(login_required)
    def post(self, request):
        movementForm = MovementForm(request.POST)

        errors = getErrors([movementForm])

        if movementForm.is_valid() and request.user.has_perm('reports.can_add_movement'):
            movement = movementForm.save(commit=False)
            movement.fk_user = request.user
            movement.dt_movement = timezone.now()

            movement.save()

            if movement.movement_type in ["R", "T"]:
                reagentBatches = ReagentBatch.objects.filter(amount__gt=0, fk_reagent=movement.fk_reagent).order_by('validity')

                if get_num_of_reagents(reagentBatches) < movement.amount:
                    movement.delete()
                    return Response(
                        {"message": "O reagente não tem tantas unidades"},
                    )

            if request.user.is_superuser:
                requestMovement = Request.objects.create(
                    dt_request=movement.dt_movement, fk_movement=movement, approved=True, dt_response=movement.dt_movement
                )
                requestMovement.save()
                if movement.movement_type == "A":
                    create_new_batch_by_movement(movement)
                elif movement.movement_type in ["R", "T"]:
                    remove_reagent_from_stock(movement)
            else:
                requestMovement = Request.objects.create(
                    dt_request=movement.dt_movement, fk_movement=movement
                )
                requestMovement.save()

            return send_request_movement(requestMovement)

        if not request.user.has_perm('reports.can_add_movement'):
            return Response(
                {"message": "Usuário não autorizado"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {"message": "Formulário incorreto"}, status=status.HTTP_400_BAD_REQUEST
        )


class ApproveRequestMovement(APIView):
    @method_decorator(login_required)
    @method_decorator(superuser_required)
    def get(self, request):
        id = request.query_params.get("id", None)

        if len(id) > 0:
            request_movement = get_object_or_404(Request, id=id)

            request_movement.approved = True
            request_movement.dt_response = timezone.now()
            request_movement.save()

            movement = request_movement.fk_movement
            reagent = movement.fk_reagent

            if movement.movement_type == "A":
                create_new_batch_by_movement(movement)
                return Response(
                    {"message" : "Requisição aprovada com sucesso"},
                    status=status.HTTP_200_OK,
                )

            elif movement.movement_type in ["R", "T"]:
                is_removed = remove_reagent_from_stock(movement)
                if is_removed:
                    return Response(
                        {"message": "Requisição aprovada com sucesso"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "A quantidade de itens no estoque é menor do que está tentando retirar"}, status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(
            {"message": "ID não fornecido"}, status=status.HTTP_400_BAD_REQUEST
        )


class DesapproveRequestMovement(APIView):
    @method_decorator(login_required)
    @method_decorator(superuser_required)
    def get(self, request):
        id = request.query_params.get("id", None)

        if len(id) >0:
            request_movement = get_object_or_404(Request, id=id)
            request_movement.dt_response = timezone.now()
            request_movement.save()

            return Response(
                {"message" : "Requisição negada com sucesso"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "ID não fornecido"}, status=status.HTTP_400_BAD_REQUEST
        )


# LICENSE

class LicensePage(View):
    def get(self, request):
        license = License.objects.filter(is_expired=False).first()
        expiredLicenses = License.objects.filter(is_expired=True).order_by("dt_register")

        context = {
            'license' : license,
            'expiredLicenses' : expiredLicenses
        }

        return render(request, 'reports/licensePage.html', context)
    
class RegisterLicense(View):
    @method_decorator(login_required)
    @method_decorator(superuser_required)
    def get(self, request):
        form = LicenseForm()

        context = {"form": form}

        return render(request, "reports/registerLicense.html", context)

    @method_decorator(login_required)
    @method_decorator(superuser_required)
    def post(self, request):
        form = LicenseForm(request.POST, request.FILES)
        errors = getErrors([form])

        if form.is_valid():
            license_instance = form.save(commit=False)
            license_instance.dt_register = date.today()
            license_instance.save()

            return redirect("/")

        context = {"form": form, "errors": errors}

        return render(request, "reports/registerLicense.html", context)


# USER


class ApproveUser(APIView):
    @method_decorator(login_required)
    @method_decorator(superuser_required)
    def get(self, request):
        codifiquedId = request.query_params.get("id", None)

        if len(codifiquedId) >0:
            decoded_id = base64.b64decode(codifiquedId).decode("utf-8")
            user = User.objects.get(id=decoded_id)

            if user:
                user.is_active = True
                user.save()
                return send_liberation_user_email(user)

            return Response(
                {"error": "User não encontrado"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"error": "ID não fornecido"}, status=status.HTTP_400_BAD_REQUEST
        )


class DisapproveUser(APIView):
    @method_decorator(login_required)
    @method_decorator(superuser_required)
    def get(self, request):
        codifiquedId = request.query_params.get("id", None)

        if len(codifiquedId) >0:
            decoded_id = base64.b64decode(codifiquedId).decode("utf-8")
            user = User.objects.get(id=decoded_id)

            if user:
                return send_cancellation_user_email(user)

            return Response(
                {"error": "User não encontrado"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"error": "ID não fornecido"}, status=status.HTTP_400_BAD_REQUEST
        )


# REPORTS

class Reports(View):
    def generate_movement_history(self, request):
        name = request.POST.get('name')
        item_status = request.POST.getlist('item_status')  # Use getlist para campos múltiplos
        start_date = request.POST.get('start_date')
        final_date = request.POST.get('final_date')

        movementsList = []
        if len(item_status) > 0:
            movements = Movement.objects.filter(
                Q(fk_reagent__state__in=item_status) &
                Q(dt_movement__gte=start_date) &
                Q(dt_movement__lte=final_date)  # Corrigido para usar final_date
            )
        else:
            movements = Movement.objects.filter(
                Q(dt_movement__gte=start_date) &
                Q(dt_movement__lte=final_date)  # Corrigido para usar final_date
            )
        
        for movement in movements:
            m_request = Request.objects.get(fk_movement=movement)

            if m_request.approved == True:
                movementsList.append(movement)

        return movementsList

    def generate_user_performace(self, request):
        user_id = request.POST.get('user')
        user = User.objects.get(id=user_id)

        name = request.POST.get('name_report_user')
        startDate = request.POST.get('start_date_user')
        finalDate = request.POST.get('final_date_user')

        movements = Movement.objects.filter(fk_user=user, dt_movement__gte=startDate, dt_movement__lte=finalDate)

        approved  = []
        denied = []

        for movement in movements:
            request_m = Request.objects.get(fk_movement=movement)

            if request_m.approved:
                approved.append(movement)
            else:
                denied.append(movement)
        
        return {
            'approved' : approved,
            'denied' : denied
        }

    def generate_siproquim_map(self, request):
        name = request.POST.get('name_report_siproquim')
        type_map = request.POST.get('type_map')
        startDate = request.POST.get('start_date_siproquim')
        finalDate = request.POST.get('final_date_siproquim')

        reagents_map = []
        reagents_verify = []
        # if type_map == 'Q':
        #     movements = Movement.objects.filter(fk_reagent__control='PF', dt_movement__gte=startDate, dt_movement__lte=finalDate)
        if type_map in ['R', 'T']:
            movements = Movement.objects.filter(fk_reagent__control='PF', dt_movement__gte=startDate, dt_movement__lte=finalDate, movement_type__in=['R', 'T'])

            for movement in movements:
                total_quantity = 0

                for batch in movement.fk_reagentBatch.all():
                    total_quantity += batch.size * movement.amount

                reagent = {
                    'name' : movement.fk_reagent.name,
                    'total_quantity' : total_quantity / 1000,
                    'category' : movement.fk_reagent.state,
                    'type_map' : 'Retirada'
                }  

                if reagent['name'] in reagents_verify:
                    index = reagents_verify.index(reagent['name'])
                    reagents_map[index]['total_quantity'] += reagent['total_quantity']
                else:
                    reagents_map.append(reagent)
                    reagents_verify.append(reagent['name'])
                
            
        else:
            movements = Movement.objects.filter(fk_reagent__control='PF', dt_movement__gte=startDate, dt_movement__lte=finalDate, movement_type='A')

            for movement in movements:
                reagent = {
                    'name' : movement.fk_reagent.name,
                    'total_quantity' : (movement.amount * movement.size) /1000,
                    'category' : movement.fk_reagent.state,
                    'type_map' : 'Adição'
                }     

                if reagent['name'] in reagents_verify:
                    index = reagents_verify.index(reagent['name'])
                    reagents_map[index]['total_quantity'] += reagent['total_quantity']
                else:
                    reagents_map.append(reagent)
                    reagents_verify.append(reagent['name'])
            
        print(reagents_map)
        return reagents_map
    
    def get(self, request):
        context = {
            'movementForm' : MovementHistoryForm(),
            'userPerformaceForm' : UserPerformanceForm(),
            'siproquimMapForm' : SiproquimMapForm()
        }
        return render(request, 'reports/reports.html', context)
    
    def post(self, request):
        submitted_form = request.POST.get('submitted_form')

        context = {
            'movementForm' : MovementHistoryForm(),
            'userPerformaceForm' : UserPerformanceForm(),
            'siproquimMapForm' : SiproquimMapForm()
        }

        if submitted_form == 'movementHistory':
            movementsList = self.generate_movement_history(request)
            context.update({'movement_history' : movementsList})

        elif submitted_form == 'userPerformace':
            userPerformace = self.generate_user_performace(request)
            context.update({'userPerformace' : userPerformace})

        elif submitted_form == 'siproquimMap':
            siproquimMap = self.generate_siproquim_map(request)
            context.update({'siproquimMap' : siproquimMap})

        return render(request, 'reports/reports.html', context)