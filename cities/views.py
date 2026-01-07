from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from cities.forms import CityForm
from cities.models import City

__all__ = (
    'CityListView', 'home', 'CityDetailView', 'CityCreateView', 'CityUpdateView',
    'CityDeleteView'
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
    paginator = Paginator(qs, 2)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'form': CityForm()}
    return render(request, 'cities/home.html', context)


class CityListView(ListView):
    model = City
    template_name = 'cities/home.html'
    paginate_by = 2


class CityDetailView(DetailView):
    model = City
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, CreateView):
    model = City
    template_name = 'cities/create.html'
    form_class = CityForm
    success_url = reverse_lazy('cities:home')

    def get_success_message(self, cleaned_data):
        message = 'Місто {name} успішно створено'
        return message.format(**cleaned_data)

class CityUpdateView(SuccessMessageMixin, UpdateView):
    model = City
    template_name = 'cities/update.html'
    form_class = CityForm
    success_url = reverse_lazy('cities:home')

    def get_success_message(self, cleaned_data):
        message = 'Місто {name} успішно відредаговано'
        return message.format(**cleaned_data)


class CityDeleteView(DeleteView):
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message({'name': self.object.name})
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        message = 'Місто {name} успішно видалено'
        return message.format(**cleaned_data)
