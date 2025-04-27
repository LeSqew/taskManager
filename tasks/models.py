from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Status(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name
class Task(models.Model):
	tittle = models.CharField(max_length=255)
	description = models.TextField()
	assigned_users = models.ManyToManyField(User, related_name='tasks', blank=True)  # Связь с пользователями
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	deadline = models.DateTimeField()
	status = models.ForeignKey(Status, on_delete=models.CASCADE)
	priority = models.IntegerField()
	difficulty = models.IntegerField()

class ScrumTable(models.Model):
	isMainTable = models.BooleanField(default=False)
	name = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	deadline = models.DateTimeField()
	Tasks = models.ManyToManyField(Task, related_name='scrum_tables', blank=True)
	assigned_users = models.ManyToManyField(User, related_name='scrum_tables', blank=True)
	assigned_tables = models.ManyToManyField('self', related_name='assigned_tables', blank=True)
	
	

