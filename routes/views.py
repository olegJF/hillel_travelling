from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from routes.forms import RouteForm

__all__ = ('home', 'find_routes')

from routes.utils import get_all_routes


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                data = get_all_routes(request, form)
            except ValueError as err:
                messages.error(request, str(err))
                return render(request, 'routes/home.html', {'form': form})
            return render(request, 'routes/home.html', data)
        return render(request, 'routes/home.html', {'form': form})
    else:
        messages.error(request, 'Немає даних для пошуку')
        return HttpResponseRedirect('/')
