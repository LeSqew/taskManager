from django.urls import path
from . import views

urlpatterns = [
    path('tables/', views.scrum_tables, name='scrum_tables'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
] 