from django.urls import path

from cities.views import *

urlpatterns = [
    # path('', CityListView.as_view(), name='home'),
    path('', home, name='home'),
    path('<int:pk>/', CityDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', CityUpdateView.as_view(), name='update'),
    path('add/', CityCreateView.as_view(), name='create'),
]
