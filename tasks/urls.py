from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tables/create/', views.create_table, name='create_table'),
    path('tables/<int:table_id>/', views.scrum_tables, name='scrum_tables'),
    path('tables/<int:table_id>/edit/', views.edit_table, name='edit_table'),
    path('tables/<int:table_id>/create_task/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
] 