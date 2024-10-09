from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from GeralUtilits import *

from .forms import *
from .models import *

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .decorators import *

# Create your views here.
class Redirect(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                return redirect('home_admin')
            else:
                return redirect('home')
        else:
            return redirect('landing_page')

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('')
        
        form = AuthenticationForm()

        context = {
            'form' : form
        }

        return render(request, 'authentication/login.html', context)
    
    def post(self, request):
        data = request.POST.copy()
        data['username'] = data['username'].lower()

        form = AuthenticationForm(request, data = data)

        errors = getErrors([form])

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        
        context = {
            "form": form,
            'errors': errors,
        }
        return render(request, 'authentication/login.html', context)
    
class RegisterUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('')
        
        registerForm = CustomUserCreationForm()

        context = {
            'form' : registerForm
        }

        return render(request, 'authentication/registerUser.html', context)
    
    def post(self, request):
        registerForm = CustomUserCreationForm(request.POST)

        errors = getErrors([registerForm])

        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.save()

            return redirect('alert_user_inactive')
        
        context = {
            'errors' : errors,
            'form' : registerForm
        }

        return render(request, 'authentication/registerUser.html', context)
    
class Users(View):
    @method_decorator(login_required)
    @method_decorator(superuser_required)
    def get(self, request):
        users = User.objects.filter()

        context = {
            'users' : users
        }

        return render(request, 'admin/usersPage.html', context)
        
        

class UserPage(View):
    @method_decorator(login_required)
    @method_decorator(superuser_required)
    def get(self, request, id):
        user = User.objects.get(id=id)
        form = PermissionForm(instance=user)

        context = {
            'userInfo' : user,
            'form' : form,
        }

        return render(request, 'admin/userPage.html', context)
    
    def post(self, request, id):
        user = User.objects.get(id=id)
        form = PermissionForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            url = reverse('user_page', kwargs={'id': id})
            return redirect(url)