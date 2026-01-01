from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from cities.models import City

__all__ = (
    'CityListView', 'home', 'CityDetailView',
)



def home(request, pk=None):
    if pk:
        city = get_object_or_404(City, id=pk)
        context = {'object': city}
        return render(request, 'cities/detail.html', context)
    qs = City.objects.all()
    context = {'objects_list': qs}
    return render(request, 'cities/home.html', context)


class CityListView(ListView):
    model = City
    template_name = 'cities/home.html'


class CityDetailView(DetailView):
    model = City
    template_name = 'cities/detail.html'
