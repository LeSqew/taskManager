from django.urls import path
from . import views

urlpatterns = [
    path('tables/<int:table_id>/create_task/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/', views.view_task, name='view_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
] 