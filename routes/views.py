from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from cities.models import City
from routes.forms import RouteForm, RouteModelForm

__all__ = ('home', 'find_routes', 'add_route')

from routes.utils import get_all_routes
from trains.models import Train


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


def add_route(request):
    if request.method == 'POST':
        data = request.POST
        total_time = int(data['total_time'])
        from_city_id = int(data['from_city'])
        to_city_id = int(data['to_city'])
        trains = data['trains'].split(',')
        train_lst = [int(t) for t in trains if t.isdigit()]
        qs = Train.objects.filter(id__in=train_lst)
        cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()
        form = RouteModelForm(
            initial={
                'total_time': total_time, 'from_city': cities[from_city_id],
                'to_city': cities[to_city_id], 'trains': qs
            }
        )
        return render(request, 'routes/create.html', {'form': form})
    else:
        messages.error(request, 'Немає даних для збереження')
        return HttpResponseRedirect('/')
