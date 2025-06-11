from django.urls import path
from . import views

urlpatterns = [
    path('task/<int:task_id>/', views.view_task, name='view_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('sprint/<int:sprint_id>/create_task/', views.create_task, name='create_task'),
	path('tasks/check_title/', views.check_task_title, name='check_task_title'),
    path('api/sprint/<int:sprint_id>/tasks/', views.sprint_tasks_api, name='sprint_tasks_api'),
] 