from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from cities.forms import CityForm
from cities.models import City

__all__ = (
    'CityListView', 'home', 'CityDetailView',
)



def home(request, pk=None):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
        qs = City.objects.all()
        context = {'object_list': qs, 'form': CityForm()}
        return render(request, 'cities/home.html', context)
    qs = City.objects.all()
    context = {'object_list': qs, 'form': CityForm()}
    return render(request, 'cities/home.html', context)


class CityListView(ListView):
    model = City
    template_name = 'cities/home.html'


class CityDetailView(DetailView):
    model = City
    template_name = 'cities/detail.html'
