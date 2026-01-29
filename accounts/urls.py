from django.urls import path

from accounts.views import *

urlpatterns = [
    path('register/', registration, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
