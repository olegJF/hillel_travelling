from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from cities.models import City
from routes.forms import RouteForm, RouteModelForm
from routes.models import Route
from routes.utils import get_all_routes
from trains.models import Train

__all__ = (
    'home', 'find_routes', 'add_route', 'save_route', 'RouteListView',
    'RouteDetailView', 'RouteDeleteView',
)


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


@login_required
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


@login_required
def save_route(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST)
        if form.is_valid():
            qs = form.cleaned_data['trains']
            route = form.save()
            route.user_id = request.user.id
            route.trains.set(qs)
            route.save()
            messages.success(request, 'Маршрут збережено')
            return HttpResponseRedirect('/')
        return render(request, 'routes/create.html', {'form': form})
    else:
        messages.error(request, 'Немає даних для збереження')
        return HttpResponseRedirect('/')


class RouteListView(LoginRequiredMixin, ListView):
    model = Route
    template_name = 'routes/list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user_id=self.request.user.id).select_related(
            'from_city', 'to_city')


class RouteDetailView(LoginRequiredMixin, DetailView):
    model = Route
    template_name = 'routes/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user_id=self.request.user.id).select_related(
            'from_city', 'to_city')


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    template_name = 'routes/delete.html'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message({'name': self.object.name})
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        message = 'Маршрут {name} успішно видалено'
        return message.format(**cleaned_data)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user_id=self.request.user.id)
