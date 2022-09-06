from .views import RegisterAPI
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
]
