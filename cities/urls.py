from django.urls import path

from cities.views import *

urlpatterns = [
    path('', CityListView.as_view(), name='home'),
    path('<int:pk>/', CityDetailView.as_view(), name='detail'),
]
