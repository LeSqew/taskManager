from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('check_email/', views.check_email, name='check_email'),
] 