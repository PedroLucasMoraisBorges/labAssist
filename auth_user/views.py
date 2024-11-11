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
            if user.is_staff or user.is_superuser:
                return redirect('home_admin')
            else:
                return redirect('home')
        else:
            return redirect('landing_page')

class Login(View):
    @method_decorator(logged_out_required)
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

class Logout(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('/')

class RegisterUser(View):
    @method_decorator(logged_out_required)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('')
        
        registerForm = CustomUserCreationForm()

        context = {
            'form' : registerForm
        }

        return render(request, 'authentication/registerUser.html', context)
    
    @method_decorator(logged_out_required)
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
        
        return render(request,'admin/usersPage.html', context)
    
    
class ViewUserProfile(View):
    @method_decorator(login_required)
    def get (self, request):
        usuario = request.user
        contexto = {
            'usuario': usuario,
        }
        return render(request, 'user_profile.html', contexto)
    
@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para editar este perfil.')
        return redirect('home')  # Redireciona para uma página padrão caso não tenha permissão

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile', username=user.username)  # Redireciona após a atualização
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'profile_edit.html', {'form': form, 'user_profile': user})
    