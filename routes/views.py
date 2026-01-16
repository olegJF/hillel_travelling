from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from routes.forms import RouteForm

__all__ = ('home', 'find_routes')


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            a = 1
        return render(request, 'routes/home.html', {'form': form})
    else:
        messages.error(request, 'Немає даних для пошуку')
        return HttpResponseRedirect('/')
