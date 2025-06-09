from django.urls import path

from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('project/create/', views.create_project, name='create_project'),
	path('project/<int:project_id>/', views.project_detail, name='project_detail'),
	path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'),
	path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
	path('project/<int:project_id>/sprint/create/', views.create_sprint, name='create_sprint'),
	path('sprint/<int:sprint_id>/', views.sprint_detail, name='sprint_detail'),
	path('sprint/<int:sprint_id>/edit/', views.edit_sprint, name='edit_sprint'),
	path('sprint/<int:sprint_id>/delete/', views.delete_sprint, name='delete_sprint'),
]
