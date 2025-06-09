from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	links = models.TextField(blank=True, help_text='Ссылки на ресурсы проекта (по одной на строку)')
	created = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
	editors = models.ManyToManyField(User, related_name='editable_projects', blank=True)
	
	class Meta:
		db_table = 'tables_Project'

	def __str__(self):
		return self.name

class Sprint(models.Model):
	name = models.CharField(max_length=255)
	start_date = models.DateTimeField(null=True, blank=True)
	deadline = models.DateTimeField()
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sprints')
	
	class Meta:
		db_table = 'tables_Sprint'

	def __str__(self):
		return self.name