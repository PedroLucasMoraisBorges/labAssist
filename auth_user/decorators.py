from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import login
from auth_user.models import User

def remember_me(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.session.get('remember_me', False):
            user_id = request.session.get('_auth_user_id')
            if user_id:
                user = User.objects.get(pk = user_id)
                login(request, user)
            else:
                return HttpResponseRedirect('login/')
        return view_func(request, *args, **kwargs)
    return wrapped_view

def admin_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrapper_func

def superuser_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser & request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrapper_func