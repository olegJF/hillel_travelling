from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from trains.forms import TrainForm
from trains.models import Train

__all__ = (
    'TrainListView', 'TrainDetailView', 'TrainCreateView', 'TrainUpdateView',
    'TrainDeleteView'
)


class TrainListView(ListView):
    model = Train
    template_name = 'trains/home.html'
    paginate_by = 10


class TrainDetailView(DetailView):
    model = Train
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Train
    template_name = 'trains/create.html'
    form_class = TrainForm
    success_url = reverse_lazy('trains:home')

    def get_success_message(self, cleaned_data):
        message = 'Поїзд {number} успішно створено'
        return message.format(**cleaned_data)

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(self.request, 'Ви не можете цього робити')
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(self.request, 'Ви не можете цього робити')
            return HttpResponseRedirect('/')
        return super().post(request, *args, **kwargs)


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Train
    template_name = 'trains/update.html'
    form_class = TrainForm
    success_url = reverse_lazy('trains:home')

    def get_success_message(self, cleaned_data):
        message = 'Поїзд {number} успішно відредаговано'
        return message.format(**cleaned_data)

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(self.request, 'Ви не можете цього робити')
            return HttpResponseRedirect('/')
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(self.request, 'Ви не можете цього робити')
            return HttpResponseRedirect('/')
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class TrainDeleteView(LoginRequiredMixin, DeleteView):
    model = Train
    template_name = 'trains/delete.html'
    success_url = reverse_lazy('trains:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message({'number': self.object.number})
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        message = 'Поїзд {number} успішно видалено'
        return message.format(**cleaned_data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(self.request, 'Ви не можете цього робити')
            return HttpResponseRedirect('/')
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(self.request, 'Ви не можете цього робити')
            return HttpResponseRedirect('/')
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)
