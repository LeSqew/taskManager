from django.urls import path

from . import views


urlpatterns = [
	path('create/', views.create_table, name='create_table'),
    path('<int:table_id>/', views.scrum_tables, name='scrum_tables'),
    path('<int:table_id>/edit/', views.edit_table, name='edit_table'),
]
