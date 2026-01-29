from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from accounts.forms import *

__all__ = ('registration', 'login_view', 'logout_view')


def registration(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return render(request, 'accounts/done.html', {'user': user})
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    form = UserLoginForm(request.POST or None)
    _next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        _next = _next or '/'
        return redirect(_next)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    messages.success(request, 'Ви вийшли з системи')
    logout(request)
    return redirect('/')
