from django.urls import path

from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('create/', views.create_table, name='create_table'),
	path('<int:table_id>/', views.sprint_table, name='scrum_tables'),
	path('<int:table_id>/edit/', views.edit_table, name='edit_table'),
	path('<int:table_id>/delete/', views.delete_table, name='delete_table'),
]
