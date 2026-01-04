from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from cities.forms import CityForm
from cities.models import City

__all__ = (
    'CityListView', 'home', 'CityDetailView', 'CityCreateView'
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


class CityCreateView(CreateView):
    model = City
    template_name = 'cities/create.html'
    form_class = CityForm
    success_url = reverse_lazy('cities:home')
